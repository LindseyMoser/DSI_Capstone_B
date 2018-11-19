## TEST JOIN QUERY

SELECT sb.SB_EIN, sb.SB_PN, sb.SB_CURR_VALUE_AST_01_AMT, sb.SB_TOT_FNDNG_TGT_AMT, form.SPONSOR_DFE_NAME, form.PLAN_NAME
FROM sb_full sb
  LEFT JOIN f5500_full form
    ON sb.SB_EIN = form.SPONS_DFE_EIN AND sb.SB_PN = form.SPONS_DFE_PN;



SELECT Book.BookID AS "Book ID" ,Book.Title AS "Book title"   
,SUM(OrderLine.quantity) AS "Number Ordered" ,ShopOrder.OrderDate AS  
"Order Date" FROM Book
INNER JOIN OrderLine ON Book.BookID = OrderLine.BookID
INNER JOIN Publisher ON Book.PublisherID = Publisher.PublisherID
INNER JOIN ShopOrder ON OrderLine.ShopOrderID = ShopOrder.ShopOrderID
WHERE Publisher.Name = 'Smith Smitheson'
GROUP BY ShopOrder.OrderDate, Name, Book.BookID
