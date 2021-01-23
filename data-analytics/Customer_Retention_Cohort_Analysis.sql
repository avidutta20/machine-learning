CREATE VIEW Starting_Month AS (
  -- (customer_id, first_month,) for each customer
  SELECT
    Customer_Id,
    MONTH(MIN(Transaction_Time)) AS Month0
  FROM
    Mutual_Fund_Transaction_Table
  WHERE
    -- Customer joining in 2019 TILL JUNE 2019
    date_format(Transaction_Time, '%Y') = '2019'
    AND MONTH(Transaction_Time) < 7 -- TILL June 2019
    AND Transaction_Status = 'Success'
  GROUP BY
    1
  ORDER BY
    2
); 
-- Customer Transaction in Month
CREATE VIEW Customer_Transaction AS (
  -- (Cust_id, start_month, Month_Number, monthly_transaction_amount)
  SELECT
    MFTXN.Customer_Id,
    Starting_Month.Month0 AS Start_Month,
    (
      MONTH(Transaction_Time) - (Starting_Month.Month0)
    ) AS Month_Number,
    
    SUM(MFTXN.No_of_Units * MFTXN.NAV_Value) AS Monthly_Transaction_Amount
  FROM
    Mutual_Fund_Transaction_Table MFTXN
    LEFT JOIN Starting_Month ON MFTXN.Customer_Id = Starting_Month.Customer_Id
  WHERE
    -- Customer joining in 2019
    date_format(Transaction_Time, '%Y') = '2019'
    AND Transaction_Status = 'Success'
    AND MONTH(Transaction_Time) < 7 -- TILL June 2019
  GROUP BY
    MFTXN.Customer_Id,
    Starting_Month.Month0,
    Month_Number
  ORDER BY
    Starting_Month.Month0,
    Month_Number
); 
-- GMV TABLE --
CREATE VIEW GMV_Retention_Table AS (
  SELECT
    CTXN.Start_Month,
    CTXN.Month_Number,
    SUM(CTXN.Monthly_Transaction_Amount) AS GMV_Value
  FROM
    Customer_Transaction CTXN
  GROUP BY
    1,
    2
  ORDER BY
    1 ASC
)