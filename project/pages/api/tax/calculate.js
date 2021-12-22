import { getIncomeTaxes } from '../../../lib/tax';

async function handler(req, res) {
  if (req.method === 'POST') {
    const {
      body: { exemptions, filingStatus, payPeriod, payRate, state },
    } = req;

    if (!exemptions) {
      res.status(400).json({
        status: 400,
        message: "The 'exemptions' vallue cannot be empty.",
      });
    }

    if (!filingStatus) {
      res.status(400).json({
        status: 400,
        message: "The 'filingStatus' vallue cannot be empty.",
      });
    }

    if (!payPeriod) {
      res.status(400).json({
        status: 400,
        message: "The 'payPeriod' vallue cannot be empty.",
      });
    }

    if (!payRate) {
      res.status(400).json({
        status: 400,
        message: "The 'payRate' vallue cannot be empty.",
      });
    }

    if (!state) {
      res.status(400).json({
        status: 400,
        message: "The 'state' vallue cannot be empty.",
      });
    }

    const payPeriodNum = getPayPeriod(payPeriod);

    if (payPeriodNum == 0) {
      res.status(400).json({
        status: 400,
        message: `Invalid payPeriod value detected: '${payPeriod}'.`,
      });
    }

    const response = await getIncomeTaxes(
      exemptions,
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
