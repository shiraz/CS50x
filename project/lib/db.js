import { MongoClient } from 'mongodb';

export async function getMongoClient() {
  const user = process.env.MONGO_DB_USERNAME;
  const pwd = process.env.MONGO_DB_PASSWORD;

  const client = await MongoClient.connect(
    `mongodb+srv://${user}:${pwd}@cluster0.iod92.mongodb.net/budgetor?retryWrites=true&w=majority`
  );
  return client;
}
