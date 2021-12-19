import { getSession } from 'next-auth/client';

import SalaryCalculate from '../components/salary-calculator/salary-calculate';

function SalaryCalculator() {
  return (
    <div id="form-container">
      <SalaryCalculate />
    </div>
  );
}

// Redirect to login if the user is not authenticated.
export async function getServerSideProps(context) {
  const session = await getSession({ req: context.req });

  if (!session) {
    return {
      redirect: {
        destination: '/auth',
        permanent: false,
      },
    };
  }

  return {
    props: {
      session,
    },
  };
}

export default SalaryCalculator;
