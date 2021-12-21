import payPeriods from './pay-periods.json';
import states from './states.json';

function Results(props) {
  const {
    payload: { payRate, payPeriod, state },
    taxData: {
      annual: {
        federal: annualFederalTaxAmount,
        fica: annualFicaTaxAmount,
        state: annualStateTaxAmount,
      },
      perPayPeriod: {
        federal: periodFederalTaxAmount,
        fica: periodFicaTaxAmount,
        state: periodStateTaxAmount,
      },
    },
  } = props;

  const currencyFormatter = new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  });

  const netPay = currencyFormatter.format(
    Math.round(
      (payRate -
        periodFederalTaxAmount -
        periodFicaTaxAmount -
        periodStateTaxAmount) *
        100
    ) / 100
  );
  const payFrequency = payPeriods.find(
    (period) => period.key === payPeriod
  ).period;
  const stateName = states.find(
    (currentState) => currentState.short === state
  ).name;

  const annualSalary = payPeriod === 'bi-weekly' ? payRate * 26 : payRate * 12;
  const annualNetPay = currencyFormatter.format(
    Math.round(
      (annualSalary -
        annualFederalTaxAmount -
        annualFicaTaxAmount -
        annualStateTaxAmount) *
        100
    ) / 100
  );

  return (
    <div className='results-container'>
      <table className='table table-bordered table-striped mt-5 w-50 mx-auto'>
        <tr>
          <th>{payFrequency} Gross Pay</th>
          <td>{currencyFormatter.format(payRate)}</td>
        </tr>
        <tr>
          <th>Federal Tax</th>
          <td>{currencyFormatter.format(periodFederalTaxAmount)}</td>
        </tr>
        <tr>
          <th>FICA Tax</th>
          <td>{currencyFormatter.format(periodFicaTaxAmount)}</td>
        </tr>
        <tr>
          <th>{stateName} State Tax</th>
          <td>{currencyFormatter.format(periodStateTaxAmount)}</td>
        </tr>
        <tr className='bg-success text-white'>
          <th>Net Pay</th>
          <td>{netPay}</td>
        </tr>
      </table>

      <table className='table table-bordered table-striped mt-5 w-50 mx-auto'>
        <tr>
          <th>Annual Gross Pay</th>
          <td>{currencyFormatter.format(annualSalary)}</td>
        </tr>
        <tr>
          <th>Annual Federal Tax</th>
          <td>{currencyFormatter.format(annualFederalTaxAmount)}</td>
        </tr>
        <tr>
          <th>Annual FICA Tax</th>
          <td>{currencyFormatter.format(annualFicaTaxAmount)}</td>
        </tr>
        <tr>
          <th>Annual {stateName} State Tax</th>
          <td>{currencyFormatter.format(annualStateTaxAmount)}</td>
        </tr>
        <tr className='bg-success text-white'>
          <th>Annual Net Pay</th>
          <td>{annualNetPay}</td>
        </tr>
      </table>
    </div>
  );
}

export default Results;
