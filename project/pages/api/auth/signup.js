import { getMongoClient } from '../../../lib/db';
import { hashPassword } from '../../../lib/auth';

async function handler(req, res) {
  if (req.method === 'POST') {
    const data = req.body;
    const { email, password } = data;

    if (
      !email ||
      !email.includes('@') ||
      !password ||
      password.trim().length < 7
    ) {
      res.status(422).json({
        message: 'Invalid input detected.',
      });
      return;
    }

    const client = await getMongoClient();
    const db = client.db();
    const hashedPwd = await hashPassword(password);

    const existingUser = await db.collection('users').findOne({
      email: email,
    });

    if (existingUser) {
      res.status(422).json({
        message: `User with the email address, '${email}' already exists.`,
      });
      return;
    }

    const result = await db.collection('users').insertOne({
      email,
      password: hashedPwd,
    });

    res.status(201).json({
      message: `User with the email address, '${email}' created successfully!`,
    });
    client.close();
  }
}

export default handler;
