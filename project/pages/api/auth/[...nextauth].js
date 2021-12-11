import NextAuth from 'next-auth';
import Providers from 'next-auth/providers';

import { getMongoClient } from '../../../lib/db';
import { verifyPassword } from '../../../lib/auth';

export default NextAuth({
  session: {
    jwt: true,
  },
  providers: [
    Providers.Credentials({
      async authorize(credentials) {
        const { email } = credentials;
        const client = await getMongoClient();
        const usersCollection = client.db().collection('users');
        const user = await usersCollection.findOne({
          email,
        });

        if (!user) {
          client.close();
          throw new Error('No user found!');
        }

        const isValid = await verifyPassword(
          credentials.password,
          user.password
        );

        if (!isValid) {
          throw new Error('Invalid password detected.');
        }

        client.close();

        return {
          email: user.email,
        };
      },
    }),
  ],
});
