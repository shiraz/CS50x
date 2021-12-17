import { getIncomeTaxes } from '../../../lib/tax';

async function handler(req, res) {
  if (req.method === 'POST') {
    const {
      body: { exemption, filingStatus, payPeriod, payRate, state },
    } = req;

    const payPeriodNum = getPayPeriod(payPeriod);

    if (payPeriodNum == 0) {
      res.status(400).json({
        status: 400,
        message: `Invalid payPeriod value detected: '${payPeriod}'.`,
      });
    }

    const response = await getIncomeTaxes(
      exemption,
      filingStatus,
      payPeriodNum,
      payRate,
      state
    );

    res.status(200).json(response);
  }
}

function getPayPeriod(payPeriod) {
    if (!payPeriod) {
        return 0;
    }
  switch (payPeriod.toLowerCase()) {
    case 'bi-weekly':
      return 26;
    case 'monthly':
      return 12;
    default:
      return 0;
  }
}

export default handler;
