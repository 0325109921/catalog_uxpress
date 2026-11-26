-- 1. Productos de un catalogo de una sucursal
--      a. Nombre de la sucursal
--      b. Nombre del catalogo
--      c. Fecha de inicio de vigencia
--      d. Fecha final de vigencia
--      e. Nombre del producto
--      f. Precio del producto
--      g. Stock
SELECT
s.nombre AS Sucursal,
c.nombre AS Catalogo,
DATE_FORMAT(c.vigenciaInicio, '%d-%m-%Y') AS VigenciaInicio,
DATE_FORMAT(c.vigenciaFin, '%d-%m-%Y') AS VigenciaFin,
p.nombre AS Producto,
cp.precio AS Precio,
st.cantStock AS Stock
FROM catalogo AS c
INNER JOIN sucursal AS s ON c.sucursal = s.codigoSucursal
INNER JOIN cat_prod AS cp ON cp.catalogo = c.numCatalogo
INNER JOIN producto AS p ON p.SKU = cp.producto
INNER JOIN stock AS st ON st.producto = p.SKU AND st.sucursal = s.codigoSucursal
WHERE s.codigoSucursal = 'S01' AND c.numCatalogo = '1';


-- 2. Informacion de un pedido
--      a. Numero del pedido
--      b. Fecha del pedido
--      c. Nombre completo del cliente
--      d. Direccion de entrega del pedido
--      e. Nombre completo del vendedor
--      f. Codigo del producto
--      g. Nombre del producto
--      h. Cantidad
--      i. Precio unitario
--      j. Importe
--      k. Subtotal
--      l. IVA
--      m. Total
SELECT
p.numPedido AS NumeroPedido,
DATE_FORMAT(p.fecha, '%d-%m-%Y') AS FechaPedido,
CONCAT(c.nombrePila, ' ', c.primerApell, ' ', IFNULL(c.segundoApell, '')) AS Cliente,
CONCAT(d.calle, ', ', d.numero, ', ', d.colonia, '') AS DireccionEntrega,
CONCAT(v.nombrePila, ' ', v.primerApell, ' ', IFNULL(v.segundoApell, '')) AS Vendedor,
pr.SKU AS CodigoProducto,
pr.nombre AS NombreProducto,
pp.cantidad AS Cantidad,
pp.precioUnitario AS PrecioUnitario,
pp.importe AS Importe,
p.subtotal AS Subtotal,
p.IVA AS IVA,
p.total AS Total
FROM pedido AS p
INNER JOIN cliente AS c ON p.cliente = c.numCliente
LEFT JOIN entrega AS e ON p.entrega = e.codigo
LEFT JOIN direccion AS d ON e.direccion = d.numDireccion
INNER JOIN vendedor AS v ON p.vendedor = v.numEmpleado
INNER JOIN ped_prod AS pp ON pp.pedido = p.numPedido
INNER JOIN producto AS pr ON pp.producto = pr.SKU
WHERE p.numPedido = 2;

-- 3. Informacion del pago del pedido
--      a. Numero de transaccion del pago
--      b. Numero de pago
--      c. Fecha del pago
--      d. Numero del pedido
--      e. Nombre completo del cliente
--      f. Concepto del pago
--      g. Monto del pago
SELECT
pg.numTransaccion AS NumeroTransaccion,
pg.numeroPago AS NumeroPago,
DATE_FORMAT(pg.fecha, '%d-%m-%Y') AS FechaPago,
pg.pedido AS NumeroPedido,
CONCAT(c.nombrePila, ' ', c.primerApell, ' ', IFNULL(c.segundoApell, '')) AS Cliente,
pg.concepto AS Concepto,
pg.monto AS Monto
FROM pago AS pg
INNER JOIN cliente AS c ON pg.cliente = c.numCliente
WHERE pg.pedido = 2;


-- 4. Informacion de la entrega de un pedido
--      a. Numero de entrega
--      b. Numero del pedido
--      c. Fecha del pedido
--      d. Fecha de entrega del pedido
--      e. Nombre completo del cliente
--      f. Direccion de entrega del pedido
--      g. Nombre completo del repartidor
SELECT
e.codigo AS NumeroEntrega,
p.numPedido AS NumeroPedido,
DATE_FORMAT(p.fecha, '%d-%m-%Y') AS FechaPedido,
DATE_FORMAT(e.fechaEntrega, '%d-%m-%Y') AS FechaEntrega,
CONCAT(c.nombrePila, ' ', c.primerApell, ' ', IFNULL(c.segundoApell, '')) AS Cliente,
CONCAT(d.calle, ', ', d.numero, ', ', d.colonia) AS DireccionEntrega,
CONCAT(r.nombrePila, ' ', r.primerApell, ' ', IFNULL(r.segundoApell, '')) AS Repartidor
FROM pedido AS p
INNER JOIN entrega AS e ON p.entrega = e.codigo
INNER JOIN cliente AS c ON p.cliente = c.numCliente
INNER JOIN direccion AS d ON e.direccion = d.numDireccion
INNER JOIN repartidor AS r ON e.repartidor = r.numRepartidor
WHERE p.numPedido = 2;


-- 5. Pedidos realizados en la misma sucursal en un periodo de tiempo
--      a. Nombre de la sucursal
--      b. Numero del pedido
--      c. Fecha del pedido
--      d. Nombre completo del cliente
--      e. Monto total del pedido
--      f. Fecha de entrega del pedido
--      g. Estado de la entrega del pedido
SELECT
s.nombre AS Sucursal,
p.numPedido AS NumeroPedido,
DATE_FORMAT(p.fecha, '%d-%m-%Y') AS FechaPedido,
CONCAT(c.nombrePila, ' ', c.primerApell, ' ', IFNULL(c.segundoApell, '')) AS Cliente,
p.total AS MontoTotal,
DATE_FORMAT(e.fechaEntrega, '%d-%m-%Y') AS FechaEntrega,
ee.descripcion AS EstadoEntrega
FROM pedido AS p
INNER JOIN catalogo AS cat ON p.catalogo = cat.numCatalogo
INNER JOIN sucursal AS s ON cat.sucursal = s.codigoSucursal
INNER JOIN cliente AS c ON p.cliente = c.numCliente
INNER JOIN entrega AS e ON p.entrega = e.codigo
INNER JOIN estado_entrega AS ee ON e.estadoEntrega = ee.codigo
WHERE s.codigoSucursal = 'S01' AND DATE(p.fecha) BETWEEN '2026-01-01' AND '2026-12-31'
ORDER BY p.fecha;