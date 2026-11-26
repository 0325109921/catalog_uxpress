-- Active: 1792076056242@@127.0.0.1@3306@catalog_uxpress
-- -------- BASE DE DATOS CATALOG UXPRESS 
-- -------- DDL
-- --------------------------------------------------------------------------------------

-- CREACION DE LA BD 
CREATE DATABASE IF NOT EXISTS catalog_uxpress;

-- Seleccionar la base de datos para crear su estructura 
USE catalog_uxpress;

-- Crear la tabla SUCURSAL
CREATE TABLE sucursal(
    codigoSucursal VARCHAR(5) PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL UNIQUE,
    dirCalle VARCHAR(100) NOT NULL,
    dirNumero VARCHAR(80) NOT NULL,
    dirColonia VARCHAR(50) NOT NULL
);

-- Crear la tabla ESTADO_ENTREGA
CREATE TABLE estado_entrega(
    codigo VARCHAR(5) PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL
);

-- Crear la tabla ESTADO_PEDIDO
CREATE TABLE estado_pedido(
    codigo VARCHAR(5) PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL
);

-- Crear la tabla REPARTIDOR
CREATE TABLE repartidor(
    numRepartidor INT PRIMARY KEY AUTO_INCREMENT,
    nombrePila VARCHAR(40) NOT NULL,
    primerApell VARCHAR(30) NOT NULL,
    segundoApell VARCHAR(30),
    dirCalle VARCHAR(100) NOT NULL,
    dirNumero VARCHAR(80) NOT NULL,
    dirColonia VARCHAR(50) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);

-- Crear la tabla CLIENTE
CREATE TABLE cliente(
    numCliente INT PRIMARY KEY AUTO_INCREMENT,
    nombrePila VARCHAR(40) NOT NULL,
    primerApell VARCHAR(30) NOT NULL,
    segundoApell VARCHAR(30)
); 

-- Crear la tabla PRODUCTO
CREATE TABLE producto(
    SKU VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(150) NOT NULL
);

-- Crear la tabla USUARIO
CREATE TABLE usuario(
    idUsuario INT PRIMARY KEY AUTO_INCREMENT,
    nombreUsuario VARCHAR(50) NOT NULL UNIQUE,
    passwordHash VARCHAR(255) NOT NULL,
    rol ENUM('ADMIN', 'VENDEDOR') NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    intentos INT NOT NULL DEFAULT 0 CHECK (intentos >= 0),
    bloqueado BOOLEAN NOT NULL DEFAULT FALSE
);

-- Crear la tabla DIRECCION
CREATE TABLE direccion(
    numDireccion INT PRIMARY KEY AUTO_INCREMENT,
    calle VARCHAR(100) NOT NULL,
    numero VARCHAR(80) NOT NULL,
    colonia VARCHAR(50) NOT NULL,
    cliente INT NOT NULL,
    FOREIGN KEY (cliente) REFERENCES cliente(numCliente)
);

-- Crear la tabla VENDEDOR 
CREATE TABLE vendedor(
    numEmpleado INT PRIMARY KEY AUTO_INCREMENT,
    nombrePila VARCHAR(40) NOT NULL,
    primerApell VARCHAR(30) NOT NULL,
    segundoApell VARCHAR(30),
    dirCalle VARCHAR(100) NOT NULL,
    dirNumero VARCHAR(80) NOT NULL,
    dirColonia VARCHAR(50) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    sucursal VARCHAR(5) NOT NULL,
    FOREIGN KEY (sucursal) REFERENCES sucursal(codigoSucursal)
);

-- Crear la tabla CATALOGO
CREATE TABLE catalogo(
    numCatalogo INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    vigenciaInicio DATE NOT NULL,
    vigenciaFin DATE,
    sucursal VARCHAR(5) NOT NULL,
    FOREIGN KEY (sucursal) REFERENCES sucursal(codigoSucursal),
    CHECK (vigenciaFin IS NULL OR vigenciaFin >= vigenciaInicio)
);

-- Crear la tabla TEL_CLIENTE
CREATE TABLE tel_cliente(
    cliente INT NOT NULL,
    numero INT NOT NULL,
    numTel VARCHAR(15) NOT NULL UNIQUE,
    PRIMARY KEY (cliente, numero),
    FOREIGN KEY (cliente) REFERENCES cliente(numCliente)
);

-- Crear la tabla TEL_VENDEDOR
CREATE TABLE tel_vendedor(
    vendedor INT NOT NULL,
    numero INT NOT NULL,
    numTel VARCHAR(15) NOT NULL UNIQUE,
    PRIMARY KEY (vendedor, numero),
    FOREIGN KEY (vendedor) REFERENCES vendedor(numEmpleado)
);

-- Crear la tabla TEL_REPARTIDOR
CREATE TABLE tel_repartidor(
    repartidor INT NOT NULL,
    numero INT NOT NULL,
    numTel VARCHAR(15) NOT NULL UNIQUE,
    PRIMARY KEY (repartidor, numero),
    FOREIGN KEY (repartidor) REFERENCES repartidor(numRepartidor)
);

-- Crear la tabla USUARIO_VENDEDOR
CREATE TABLE usuario_vendedor(
    usuario INT NOT NULL UNIQUE,
    vendedor INT NOT NULL UNIQUE,
    PRIMARY KEY (usuario, vendedor),
    FOREIGN KEY (usuario) REFERENCES usuario(idUsuario),
    FOREIGN KEY (vendedor) REFERENCES vendedor(numEmpleado)
);

-- Crear la tabla ENTREGA
CREATE TABLE entrega(
    codigo INT PRIMARY KEY AUTO_INCREMENT,
    fechaEntrega DATE NOT NULL,
    entregaConfirmada BOOLEAN NOT NULL DEFAULT FALSE,
    estadoEntrega VARCHAR(5) NOT NULL,
    sucursal VARCHAR(5) NOT NULL,
    repartidor INT NULL,
    direccion INT NOT NULL,
    FOREIGN KEY (estadoEntrega) REFERENCES estado_entrega(codigo),
    FOREIGN KEY (sucursal) REFERENCES sucursal(codigoSucursal),
    FOREIGN KEY (repartidor) REFERENCES repartidor(numRepartidor),
    FOREIGN KEY (direccion) REFERENCES direccion(numDireccion)
);

-- Crear la tabla CAT_PROD
CREATE TABLE cat_prod(
    catalogo INT NOT NULL,
    producto VARCHAR(20) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio > 0),
    PRIMARY KEY (catalogo, producto),
    FOREIGN KEY (catalogo) REFERENCES catalogo(numCatalogo),
    FOREIGN KEY (producto) REFERENCES producto(SKU)
);

CREATE TABLE stock(
    sucursal VARCHAR(5) NOT NULL,
    producto VARCHAR(20) NOT NULL,
    cantStock INT NOT NULL DEFAULT 0 CHECK (cantStock >= 0),
    PRIMARY KEY (sucursal, producto),
    FOREIGN KEY (sucursal) REFERENCES sucursal(codigoSucursal),
    FOREIGN KEY (producto) REFERENCES producto(SKU)
);

-- Crear la tabla PEDIDO
CREATE TABLE pedido(
    numPedido INT PRIMARY KEY AUTO_INCREMENT,
    fecha DATETIME NOT NULL,
    cantArticulos INT NOT NULL CHECK (cantArticulos > 0),
    subtotal DECIMAL(10, 2) NOT NULL CHECK (subtotal >= 0),
    IVA DECIMAL(10, 2) NOT NULL CHECK (IVA >= 0),
    total DECIMAL(10, 2) NOT NULL CHECK (total >= 0),
    catalogo INT NOT NULL,
    vendedor INT NOT NULL,
    estadoPedido VARCHAR(5) NOT NULL,
    entrega INT NOT NULL,
    cliente INT NOT NULL,
    FOREIGN KEY (catalogo) REFERENCES catalogo(numCatalogo),
    FOREIGN KEY (vendedor) REFERENCES vendedor(numEmpleado),
    FOREIGN KEY (estadoPedido) REFERENCES estado_pedido(codigo),
    FOREIGN KEY (entrega) REFERENCES entrega(codigo),
    FOREIGN KEY (cliente) REFERENCES cliente(numCliente),
    UNIQUE (numPedido, catalogo)
);

-- Crear la tabla PED_PROD
CREATE TABLE ped_prod(
    pedido INT NOT NULL,
    catalogo INT NOT NULL,
    producto VARCHAR(20) NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precioUnitario DECIMAL(10, 2) NOT NULL CHECK (precioUnitario > 0),
    importe DECIMAL(10, 2) NOT NULL CHECK (importe > 0),
    PRIMARY KEY (pedido, producto),
    FOREIGN KEY (pedido, catalogo) REFERENCES pedido(numPedido, catalogo),
    FOREIGN KEY (catalogo, producto) REFERENCES cat_prod(catalogo, producto)
);

-- Crear la tabla PAGO
CREATE TABLE pago(
    numTransaccion INT PRIMARY KEY AUTO_INCREMENT,
    concepto VARCHAR(100) NOT NULL,
    fecha DATETIME NOT NULL,
    monto DECIMAL(10, 2) NOT NULL CHECK (monto > 0),
    numeroPago INT NOT NULL CHECK (numeroPago > 0),
    saldo DECIMAL(10, 2) NOT NULL CHECK (saldo >= 0),
    pedido INT NOT NULL,
    cliente INT NOT NULL,
    FOREIGN KEY (pedido) REFERENCES pedido(numPedido),
    FOREIGN KEY (cliente) REFERENCES cliente(numCliente)
);