import { getSession } from 'next-auth/client';

function SalaryCalculator() {
  return <p>TO DO</p>;
}

// Redirect to login if the user is not authenticated.
export async function getServerSideProps(context) {
  const session = await getSession({req: context.req});

  if (!session) {
    return {
      redirect: {
        destination: '/auth',
        permanent: false,
      }
    };
  }

  return {
    props: {
      session
    }
  };
}

export default SalaryCalculator;
