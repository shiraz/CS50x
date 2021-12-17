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

  const { status } = response;

  if (status !== 200) {
    return {
      status,
      message: response.statusText,
    };
  }

  const jsonResponse = await response.json();

  const { annual, per_pay_period: perPayPeriod } = jsonResponse;
  const perPayPeriodRounded = {
    federal: Math.round(perPayPeriod.federal.amount * 1e2) / 1e2,
    state: Math.round(perPayPeriod.state.amount * 1e2) / 1e2,
    fica: Math.round(perPayPeriod.fica.amount * 1e2) / 1e2,
  };

  return {
    status,
    annual: {
      federal: annual.federal.amount,
      state: annual.state.amount,
      fica: annual.fica.amount,
    },
    perPayPeriod: perPayPeriodRounded,
  };
}