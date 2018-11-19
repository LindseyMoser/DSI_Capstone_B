## TEST JOIN QUERY

SELECT sb.SB_EIN, sb.SB_PN, sb.SB_CURR_VALUE_AST_01_AMT, sb.SB_TOT_FNDNG_TGT_AMT, sb.SB_PLAN_YEAR_BEGIN_DATE, sb.SB_EFF_INT_RATE_PRCNT,
        form.SPONSOR_DFE_NAME, form.PLAN_NAME, form.SHORT_PLAN_YR_IND, form.COLLECTIVE_BARGAIN_IND,
        h.TOT_ASSETS_BOY_AMT, h.TOT_ASSETS_EOY_AMT, h.TOT_LIABILITIES_BOY_AMT, h.TOT_LIABILITIES_EOY_AMT, h.NET_ASSETS_BOY_AMT, h.NET_ASSETS_EOY_AMT
FROM sb_full sb
  LEFT JOIN f5500_full form
    ON sb.SB_EIN = form.SPONS_DFE_EIN AND sb.SB_PN = form.SPONS_DFE_PN
  LEFT JOIN h_full h
    ON sb.SB_EIN = h.SCH_H_EIN AND sb.SB_PN = h.SCH_H_PN
  WHERE sb.SB_PLAN_YEAR_BEGIN_DATE BETWEEN '2017-01-01' AND '2017-12-31';



SELECT Book.BookID AS "Book ID" ,Book.Title AS "Book title"   
,SUM(OrderLine.quantity) AS "Number Ordered" ,ShopOrder.OrderDate AS  
"Order Date" FROM Book
INNER JOIN OrderLine ON Book.BookID = OrderLine.BookID
INNER JOIN Publisher ON Book.PublisherID = Publisher.PublisherID
INNER JOIN ShopOrder ON OrderLine.ShopOrderID = ShopOrder.ShopOrderID
WHERE Publisher.Name = 'Smith Smitheson'
GROUP BY ShopOrder.OrderDate, Name, Book.BookID
