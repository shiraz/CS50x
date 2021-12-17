export async function getIncomeTaxes(
  exemption,
  filingStatus,
  payPeriod,
  payRate,
  state
) {
  process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

  const response = await fetch('https://taxee.io/api/v2/calculate/2020', {
    method: 'POST',
    body: JSON.stringify({
      exemptions: exemption,
      filing_status: filingStatus,
      pay_periods: payPeriod,
      pay_rate: payRate,
      state,
    }),
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.TAXEE_API_KEY}`,
    },
  });

  const jsonResponse = await response.json();

  return {
    status: response.status,
    ...jsonResponse,
  };
}
