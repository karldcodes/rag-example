
using OpenAI.Chat;
using OpenAI.Embeddings;
using Npgsql;
using Pgvector;
using Pgvector.Npgsql;
using NpgsqlTypes;

var openAiKey = Environment.GetEnvironmentVariable("OPENAI_API_KEY")
    ?? throw new Exception("OPENAI_API_KEY is missing.");

var connectionString = Environment.GetEnvironmentVariable("DATABASE_URL")
    ?? "Host=postgres;Port=5432;Username=admin;Password=password;Database=rag_db";

// create database builder and enable vectors
var dataSourceBuilder = new NpgsqlDataSourceBuilder(connectionString);
dataSourceBuilder.UseVector();

await using var dataSource = dataSourceBuilder.Build();
await using var conn = await dataSource.OpenConnectionAsync();

// create a text embedding of the question so we can use it to check the vector db for related data
// in this example we hard code it but this will come from the user

var question = "What provides the greatest precision of all the EQ plugins?";


Console.WriteLine("Question");
Console.WriteLine(question);

var embeddingClient = new EmbeddingClient("text-embedding-3-small", openAiKey);
OpenAIEmbedding embedding = embeddingClient.GenerateEmbedding(question);
var vector = new Vector(embedding.ToFloats().ToArray());

await using var cmd = new NpgsqlCommand(
    """
    SELECT content
    FROM document_chunks
    ORDER BY embedding <=> @embedding
    LIMIT 5;
    """,
    conn
);

cmd.Parameters.AddWithValue("embedding", vector);

await using var reader = await cmd.ExecuteReaderAsync();

// create context for use in prompt from data pulled back from database
var contextChunks = new List<string>();
while (await reader.ReadAsync())
{
    contextChunks.Add(reader.GetString(0));
}
var context = string.Join("\n\n---\n\n", contextChunks);


var messages = new ChatMessage[]
{
    new SystemChatMessage(
        """
        You are a helpful assistant. Answer the user's question using the provided context.
        If the answer is not in the context, say you don't know based on the provided documents.
        """
    ),
    new UserChatMessage(
        $"""
        Context:

        {context}

        Question:

        {question}
        """
    )
};

var chatClient = new ChatClient("gpt-5-nano", openAiKey);
var completion = await chatClient.CompleteChatAsync(messages);

Console.WriteLine();
Console.WriteLine(completion.Value.Content[0].Text);
