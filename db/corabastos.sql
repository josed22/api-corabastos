-- =====================================================================
-- CORABASTOS - Base de datos principal (PostgreSQL)
-- 16 tablas + 2 vistas + datos de ejemplo.
-- Ejecutar completo, de una sola vez, en una base VACÍA
-- (pgAdmin: clic derecho en la base > Query Tool > pegar > F5).
-- Contraseña de todos los usuarios de ejemplo: Clave2025*
-- =====================================================================

CREATE OR REPLACE FUNCTION set_actualizado() RETURNS TRIGGER AS $$
BEGIN NEW.actualizado = CURRENT_TIMESTAMP; RETURN NEW; END;
$$ LANGUAGE plpgsql;

-- ---------------------------- TABLAS ---------------------------------
CREATE TABLE rol (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(60) NOT NULL UNIQUE,
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE modulo (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(50) NOT NULL UNIQUE,
  descripcion TEXT,
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE modulo_x_rol (
  id SERIAL PRIMARY KEY,
  id_rol INTEGER NOT NULL REFERENCES rol(id),
  id_modulo INTEGER NOT NULL REFERENCES modulo(id),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_modulo_x_rol UNIQUE (id_rol, id_modulo)
);

CREATE TABLE municipio (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(80) NOT NULL UNIQUE,
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tipo_identificacion (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(60) NOT NULL UNIQUE,
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE usuario (
  id SERIAL PRIMARY KEY,
  id_rol INTEGER NOT NULL REFERENCES rol(id),
  id_municipio INTEGER NOT NULL REFERENCES municipio(id),
  id_tipo_identificacion INTEGER NOT NULL REFERENCES tipo_identificacion(id),
  nombre VARCHAR(40) NOT NULL,
  apellido VARCHAR(40) NOT NULL,
  correo VARCHAR(150) NOT NULL UNIQUE,
  direccion VARCHAR(100) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  numero_identificacion VARCHAR(30) NOT NULL UNIQUE,
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categoria (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL UNIQUE,
  descripcion VARCHAR(500),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tipo (
  id SERIAL PRIMARY KEY,
  id_categoria INTEGER NOT NULL REFERENCES categoria(id),
  nombre VARCHAR(100) NOT NULL UNIQUE,
  descripcion VARCHAR(500),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE producto (
  id SERIAL PRIMARY KEY,
  id_tipo INTEGER NOT NULL REFERENCES tipo(id),
  codigo VARCHAR(30) NOT NULL UNIQUE,
  nombre VARCHAR(100) NOT NULL,
  unidad_medida VARCHAR(20) NOT NULL DEFAULT 'kg',
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pabellon (
  id SERIAL PRIMARY KEY,
  id_categoria INTEGER NOT NULL REFERENCES categoria(id),
  nombre VARCHAR(80) NOT NULL UNIQUE,
  descripcion VARCHAR(300),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tienda (
  id SERIAL PRIMARY KEY,
  id_usuario INTEGER NOT NULL REFERENCES usuario(id),      -- vendedor dueño
  id_pabellon INTEGER NOT NULL REFERENCES pabellon(id),
  nombre VARCHAR(100) NOT NULL UNIQUE,
  numero_local VARCHAR(20) NOT NULL,
  telefono VARCHAR(20),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_tienda_local UNIQUE (id_pabellon, numero_local)
);

CREATE TABLE inventario (
  id SERIAL PRIMARY KEY,
  id_tienda INTEGER NOT NULL REFERENCES tienda(id),
  id_producto INTEGER NOT NULL REFERENCES producto(id),
  cantidad_disponible NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (cantidad_disponible >= 0),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_inventario UNIQUE (id_tienda, id_producto)
);

CREATE TABLE precio_dia (
  id SERIAL PRIMARY KEY,
  id_producto INTEGER NOT NULL REFERENCES producto(id),
  id_usuario INTEGER NOT NULL REFERENCES usuario(id),      -- administrador que fija el precio
  fecha DATE NOT NULL DEFAULT CURRENT_DATE,
  precio NUMERIC(12,2) NOT NULL CHECK (precio > 0),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_precio_dia UNIQUE (id_producto, fecha)
);

CREATE TABLE estado_reserva (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(40) NOT NULL UNIQUE,
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reserva (
  id SERIAL PRIMARY KEY,
  id_usuario INTEGER NOT NULL REFERENCES usuario(id),      -- comprador
  id_tienda INTEGER NOT NULL REFERENCES tienda(id),
  id_estado_reserva INTEGER NOT NULL REFERENCES estado_reserva(id),
  codigo VARCHAR(30) NOT NULL UNIQUE,
  fecha_retiro DATE NOT NULL,
  observacion VARCHAR(300),
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE detalle_reserva (
  id SERIAL PRIMARY KEY,
  id_reserva INTEGER NOT NULL REFERENCES reserva(id),
  id_producto INTEGER NOT NULL REFERENCES producto(id),
  cantidad NUMERIC(10,2) NOT NULL CHECK (cantidad > 0),
  precio_unitario NUMERIC(12,2) NOT NULL,                  -- precio del día al apartar
  estado BOOLEAN NOT NULL DEFAULT TRUE,
  creado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  actualizado TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_detalle_reserva UNIQUE (id_reserva, id_producto)
);

-- --------------- TRIGGER "actualizado" EN TODAS LAS TABLAS -----------
DO $$
DECLARE t TEXT;
BEGIN
  FOREACH t IN ARRAY ARRAY['rol','modulo','modulo_x_rol','municipio','tipo_identificacion',
    'usuario','categoria','tipo','producto','pabellon','tienda','inventario',
    'precio_dia','estado_reserva','reserva','detalle_reserva']
  LOOP
    EXECUTE format('CREATE TRIGGER trg_%I_actualizado BEFORE UPDATE ON %I
                    FOR EACH ROW EXECUTE FUNCTION set_actualizado()', t, t);
  END LOOP;
END $$;

-- ------------------------------ DATOS --------------------------------
INSERT INTO rol (nombre) VALUES ('Administrador'), ('Vendedor'), ('Comprador');

INSERT INTO modulo (nombre, descripcion) VALUES
('Dashboard',            'Resumen de precios, inventario y reservas'),
('Usuarios',             'Gestión de usuarios del sistema'),
('Roles y Módulos',      'Asignación de módulos por rol'),
('Categorías y Tipos',   'Clasificación de productos'),
('Productos',            'Catálogo maestro de productos'),
('Precios del Día',      'Precios diarios y su variación porcentual'),
('Tiendas y Pabellones', 'Pabellones y tiendas de Corabastos'),
('Inventario',           'Cantidad disponible de cada producto en la tienda'),
('Reservas',             'Reservas recibidas de compradores'),
('Reportes',             'Reportes de precios y reservas'),
('Catálogo',             'Búsqueda de productos y tiendas que los tienen'),
('Mis Reservas',         'Productos apartados por el comprador');

INSERT INTO modulo_x_rol (id_rol, id_modulo)
SELECT r.id, m.id
FROM (VALUES
  ('Administrador','Dashboard'), ('Administrador','Usuarios'), ('Administrador','Roles y Módulos'),
  ('Administrador','Categorías y Tipos'), ('Administrador','Productos'), ('Administrador','Precios del Día'),
  ('Administrador','Tiendas y Pabellones'), ('Administrador','Reportes'),
  ('Vendedor','Dashboard'), ('Vendedor','Catálogo'), ('Vendedor','Precios del Día'),
  ('Vendedor','Inventario'), ('Vendedor','Reservas'),
  ('Comprador','Catálogo'), ('Comprador','Precios del Día'), ('Comprador','Mis Reservas')
) v(rol, modulo)
JOIN rol r ON r.nombre = v.rol
JOIN modulo m ON m.nombre = v.modulo;

INSERT INTO municipio (nombre) VALUES
('Bogotá'),('Cajicá'),('Chía'),('Soacha'),('Zipaquirá'),('Facatativá'),
('Fusagasugá'),('Girardot'),('Funza'),('Mosquera'),('Madrid');

INSERT INTO tipo_identificacion (nombre) VALUES
('Cédula de ciudadanía'),('Cédula de extranjería'),('Pasaporte'),('NIT'),('Permiso de residencia');

-- ids: 1 admin, 2-9 vendedores, 10-14 compradores
INSERT INTO usuario (id_rol, id_municipio, id_tipo_identificacion, nombre, apellido, correo, direccion, password_hash, numero_identificacion) VALUES
(1, 1, 1, 'Laura',      'Gómez Rincón',     'laura.gomez@gmail.com',      'Cra 15 # 93-40',         'Clave2025*', '1020456789'),
(2, 3, 1, 'Carlos',     'Rodríguez Pardo',  'carlos.rodriguez@gmail.com', 'Calle 12 # 8-25',        'Clave2025*', '80123456'),
(2, 4, 1, 'Ricardo',    'Ospina Mejía',     'ricardo.ospina@gmail.com',   'Cra 7 # 12-40',          'Clave2025*', '79456123'),
(2, 5, 1, 'Marcela',    'Torres Ávila',     'marcela.torres@hotmail.com', 'Cra 7 # 4-60',           'Clave2025*', '52987654'),
(2, 1, 1, 'Andrea',     'Salazar Londoño',  'andrea.salazar@gmail.com',   'Calle 40 Sur # 78-15',   'Clave2025*', '1032654987'),
(2, 9, 1, 'Jorge',      'Beltrán Cruz',     'jorge.beltran@gmail.com',    'Cra 9 # 14-22',          'Clave2025*', '19876543'),
(2, 6, 1, 'Luz Marina', 'Quintero Páez',    'luz.quintero@outlook.com',   'Calle 5 # 3-18',         'Clave2025*', '51234890'),
(2, 10,1, 'Hernán',     'Díaz Vargas',      'hernan.diaz@gmail.com',      'Cra 3 # 8-30',           'Clave2025*', '79321654'),
(2, 1, 1, 'Gloria',     'Patiño Ruiz',      'gloria.patino@hotmail.com',  'Cra 80 # 38 Sur-12',     'Clave2025*', '41567832'),
(3, 2, 1, 'Andrés',     'Martínez Silva',   'andres.martinez@gmail.com',  'Calle 3 # 5-18',         'Clave2025*', '1013567890'),
(3, 4, 1, 'Daniela',    'Peña Castro',      'daniela.pena@outlook.com',   'Diag 32 # 10-45',        'Clave2025*', '1032456123'),
(3, 7, 1, 'Julián',     'Herrera Mora',     'julian.herrera@gmail.com',   'Cra 68 # 24-30',         'Clave2025*', '1075432198'),
(3, 11,1, 'Valentina',  'Ruiz Cortés',      'valentina.ruiz@gmail.com',   'Cra 5 # 12-30',          'Clave2025*', '1098765432'),
(3, 8, 1, 'Camilo',     'Sánchez Ortiz',    'camilo.sanchez@hotmail.com', 'Calle 18 # 9-40',        'Clave2025*', '1110456789');

INSERT INTO categoria (nombre, descripcion) VALUES
('Granos',            'Arroz, fríjol, lentejas y cereales'),
('Frutas',            'Frutas frescas de clima cálido y frío'),
('Verduras',          'Hortalizas y verduras frescas'),
('Tubérculos',        'Papas y raíces'),
('Lácteos y huevos',  'Leche, quesos y huevos'),
('Carnes',            'Carne de res, pollo y cerdo');

INSERT INTO tipo (id_categoria, nombre, descripcion) VALUES
(1, 'Arroz',               'Arroz blanco e integral'),
(1, 'Fríjol',              'Variedades de fríjol seco'),
(1, 'Lentejas y garbanzo', 'Leguminosas secas'),
(1, 'Cereales',            'Maíz, avena y quinua'),
(2, 'Cítricos',            'Naranja, limón y mandarina'),
(2, 'Tropicales',          'Frutas de clima cálido'),
(2, 'Clima frío',          'Frutas de tierra fría'),
(3, 'Hortalizas',          'Tomate, zanahoria y similares'),
(3, 'De hoja',             'Lechuga, repollo y espinaca'),
(3, 'Bulbos',              'Cebolla y ajo'),
(4, 'Papas',               'Variedades de papa'),
(4, 'Raíces',              'Yuca, arracacha y ñame'),
(5, 'Huevos',              'Huevo por cubeta'),
(5, 'Lácteos',             'Leche y quesos'),
(6, 'Res',                 'Cortes de res'),
(6, 'Pollo',               'Pollo entero y presas'),
(6, 'Cerdo',               'Cortes de cerdo');

INSERT INTO pabellon (id_categoria, nombre, descripcion) VALUES
(1, 'Pabellón de Granos',          'Bodegas de granos y cereales'),
(2, 'Pabellón de Frutas',          'Bodegas de frutas frescas'),
(3, 'Pabellón de Verduras',        'Bodegas de hortalizas y verduras'),
(4, 'Pabellón de Tubérculos',      'Bodegas de papa y raíces'),
(5, 'Pabellón de Lácteos y Huevos','Bodegas de lácteos y huevos'),
(6, 'Pabellón de Carnes',          'Bodegas de carnes frías y frescas');

INSERT INTO tienda (id_usuario, id_pabellon, nombre, numero_local, telefono) VALUES
(2, 1, 'Granos El Campesino',             'G-20', '3105551201'),
(3, 1, 'Granos y Cereales Don Pedro',     'G-34', '3115551202'),
(4, 2, 'Frutas La Cosecha',               'F-12', '3125551203'),
(5, 2, 'Frutas Tropicales del Tolima',    'F-27', '3135551204'),
(6, 3, 'Verduras Hortalizas Sabana',      'V-08', '3145551205'),
(7, 4, 'Tubérculos Papa Criolla Boyacá',  'T-15', '3155551206'),
(8, 5, 'Lácteos y Huevos Los Andes',      'L-05', '3165551207'),
(9, 6, 'Carnes Frigorífico Central',      'C-03', '3175551208');

INSERT INTO estado_reserva (nombre) VALUES ('Pendiente'),('Confirmada'),('Retirada'),('Cancelada');

-- Productos (50) + precios de los últimos 7 días (fijados por el administrador).
-- El precio de cada día fluctúa: más en verduras y frutas, menos en granos y lácteos.
WITH datos (codigo, tipo_nombre, nombre, unidad, precio_ref) AS (VALUES
 ('GRA-001','Arroz','Arroz blanco premium','kg',3800),
 ('GRA-002','Arroz','Arroz integral','kg',4600),
 ('GRA-003','Fríjol','Fríjol cargamanto rojo','kg',9800),
 ('GRA-004','Fríjol','Fríjol bola roja','kg',8900),
 ('GRA-005','Fríjol','Fríjol zaragoza','kg',8200),
 ('GRA-006','Lentejas y garbanzo','Lenteja','kg',5200),
 ('GRA-007','Lentejas y garbanzo','Garbanzo','kg',6800),
 ('GRA-008','Lentejas y garbanzo','Arveja seca verde','kg',4900),
 ('GRA-009','Cereales','Maíz amarillo trillado','kg',3400),
 ('GRA-010','Cereales','Avena en hojuelas','kg',5600),
 ('GRA-011','Cereales','Quinua','kg',9500),
 ('FRU-001','Cítricos','Naranja Valencia','kg',2400),
 ('FRU-002','Cítricos','Limón Tahití','kg',3200),
 ('FRU-003','Cítricos','Mandarina Oneco','kg',3000),
 ('FRU-004','Tropicales','Banano criollo','kg',2100),
 ('FRU-005','Tropicales','Mango Tommy','kg',3800),
 ('FRU-006','Tropicales','Piña perolera','kg',2600),
 ('FRU-007','Tropicales','Papaya Maradol','kg',2900),
 ('FRU-008','Clima frío','Fresa','kg',6500),
 ('FRU-009','Clima frío','Mora de Castilla','kg',7200),
 ('FRU-010','Clima frío','Tomate de árbol','kg',3900),
 ('FRU-011','Tropicales','Aguacate Hass','kg',8500),
 ('VER-001','Hortalizas','Tomate chonto','kg',2800),
 ('VER-002','Hortalizas','Zanahoria','kg',1800),
 ('VER-003','Hortalizas','Habichuela','kg',3500),
 ('VER-004','Hortalizas','Pimentón rojo','kg',4200),
 ('VER-005','De hoja','Lechuga batavia','unidad',1500),
 ('VER-006','De hoja','Repollo blanco','kg',1500),
 ('VER-007','De hoja','Espinaca','kg',3600),
 ('VER-008','Bulbos','Cebolla cabezona blanca','kg',2300),
 ('VER-009','Bulbos','Cebolla larga junca','kg',2700),
 ('VER-010','Bulbos','Ajo','kg',12500),
 ('VER-011','Hortalizas','Remolacha','kg',2000),
 ('VER-012','Hortalizas','Pepino cohombro','kg',2200),
 ('TUB-001','Papas','Papa pastusa','kg',1700),
 ('TUB-002','Papas','Papa criolla','kg',3300),
 ('TUB-003','Papas','Papa sabanera','kg',1900),
 ('TUB-004','Raíces','Yuca','kg',1600),
 ('TUB-005','Raíces','Arracacha','kg',2800),
 ('TUB-006','Raíces','Ñame','kg',3000),
 ('LAC-001','Huevos','Huevo rojo AA cubeta x30','cubeta',17500),
 ('LAC-002','Huevos','Huevo blanco A cubeta x30','cubeta',15500),
 ('LAC-003','Lácteos','Leche entera cruda','litro',2600),
 ('LAC-004','Lácteos','Queso campesino','kg',14500),
 ('LAC-005','Lácteos','Cuajada','kg',11000),
 ('CAR-001','Res','Carne molida de res','kg',21000),
 ('CAR-002','Pollo','Pollo entero','kg',9800),
 ('CAR-003','Pollo','Pechuga de pollo','kg',13500),
 ('CAR-004','Cerdo','Costilla de cerdo','kg',16500),
 ('CAR-005','Cerdo','Chuleta de cerdo','kg',15500)
),
nuevos AS (
  INSERT INTO producto (id_tipo, codigo, nombre, unidad_medida)
  SELECT t.id, dt.codigo, dt.nombre, dt.unidad
  FROM datos dt JOIN tipo t ON t.nombre = dt.tipo_nombre
  RETURNING id, codigo
)
INSERT INTO precio_dia (id_producto, id_usuario, fecha, precio)
SELECT n.id,
       (SELECT id FROM usuario WHERE correo = 'laura.gomez@gmail.com'),
       CURRENT_DATE - g.dia,
       GREATEST(50, ROUND((dt.precio_ref * (1 + a.amp * SIN(n.id * 2.3 + g.dia * 1.3)))::numeric / 50) * 50)
FROM nuevos n
JOIN datos dt ON dt.codigo = n.codigo
JOIN tipo t ON t.nombre = dt.tipo_nombre
JOIN categoria c ON c.id = t.id_categoria
CROSS JOIN generate_series(0, 6) AS g(dia)
CROSS JOIN LATERAL (SELECT CASE c.nombre
    WHEN 'Verduras' THEN 0.25 WHEN 'Frutas' THEN 0.18 WHEN 'Tubérculos' THEN 0.15
    WHEN 'Carnes' THEN 0.07 WHEN 'Granos' THEN 0.05 ELSE 0.04 END AS amp) a;

-- Inventario: cada tienda solo tiene productos de la categoría de su pabellón
INSERT INTO inventario (id_tienda, id_producto, cantidad_disponible)
SELECT ti.id, p.id,
       CASE WHEN (p.id + ti.id) % 7 = 0 THEN 0
            ELSE 50 + ((p.id * 37 + ti.id * 91) % 950) END
FROM tienda ti
JOIN pabellon pa ON pa.id = ti.id_pabellon
JOIN tipo t      ON t.id_categoria = pa.id_categoria
JOIN producto p  ON p.id_tipo = t.id
WHERE (p.id + ti.id) % 3 <> 0;

-- ------------------------------ VISTAS -------------------------------
-- Precio de cada día con el precio anterior y el % de subida o bajada
CREATE VIEW v_variacion_precio AS
SELECT x.id_producto, x.codigo, x.producto, x.categoria, x.unidad_medida, x.fecha,
       x.precio, x.precio_anterior,
       CASE WHEN x.precio_anterior IS NULL THEN NULL
            ELSE ROUND((x.precio - x.precio_anterior) / x.precio_anterior * 100, 2) END AS variacion_pct,
       CASE WHEN x.precio_anterior IS NULL OR x.precio = x.precio_anterior THEN 'igual'
            WHEN x.precio > x.precio_anterior THEN 'sube' ELSE 'baja' END AS tendencia
FROM (
  SELECT pd.id_producto, p.codigo, p.nombre AS producto, c.nombre AS categoria,
         p.unidad_medida, pd.fecha, pd.precio,
         LAG(pd.precio) OVER (PARTITION BY pd.id_producto ORDER BY pd.fecha) AS precio_anterior
  FROM precio_dia pd
  JOIN producto p  ON p.id = pd.id_producto
  JOIN tipo t      ON t.id = p.id_tipo
  JOIN categoria c ON c.id = t.id_categoria
  WHERE pd.estado
) x;

-- Lo que ve el comprador hoy: qué tienda tiene el producto, a qué precio y cuánto subió o bajó
CREATE VIEW v_catalogo_hoy AS
SELECT p.id AS id_producto, p.nombre AS producto, v.categoria, p.unidad_medida,
       ti.id AS id_tienda, ti.nombre AS tienda, pa.nombre AS pabellon, ti.numero_local,
       i.cantidad_disponible,
       v.precio AS precio_hoy, v.precio_anterior, v.variacion_pct, v.tendencia
FROM inventario i
JOIN tienda ti  ON ti.id = i.id_tienda
JOIN pabellon pa ON pa.id = ti.id_pabellon
JOIN producto p ON p.id = i.id_producto
JOIN v_variacion_precio v ON v.id_producto = p.id AND v.fecha = CURRENT_DATE
WHERE i.estado AND ti.estado AND p.estado;

-- Reservas de ejemplo (el comprador aparta, no compra)
INSERT INTO reserva (id_usuario, id_tienda, id_estado_reserva, codigo, fecha_retiro, observacion) VALUES
((SELECT id FROM usuario WHERE correo='andres.martinez@gmail.com'), (SELECT id FROM tienda WHERE nombre='Granos El Campesino'),            (SELECT id FROM estado_reserva WHERE nombre='Pendiente'),  'RES-0001', CURRENT_DATE + 1, 'Retiro en la mañana, bodega G-20'),
((SELECT id FROM usuario WHERE correo='daniela.pena@outlook.com'),  (SELECT id FROM tienda WHERE nombre='Verduras Hortalizas Sabana'),    (SELECT id FROM estado_reserva WHERE nombre='Confirmada'), 'RES-0002', CURRENT_DATE + 1, 'Llego con camión propio'),
((SELECT id FROM usuario WHERE correo='julian.herrera@gmail.com'),  (SELECT id FROM tienda WHERE nombre='Tubérculos Papa Criolla Boyacá'),(SELECT id FROM estado_reserva WHERE nombre='Retirada'),   'RES-0003', CURRENT_DATE - 1, NULL),
((SELECT id FROM usuario WHERE correo='valentina.ruiz@gmail.com'),  (SELECT id FROM tienda WHERE nombre='Frutas La Cosecha'),            (SELECT id FROM estado_reserva WHERE nombre='Cancelada'),  'RES-0004', CURRENT_DATE,     'Cancelada por el comprador'),
((SELECT id FROM usuario WHERE correo='camilo.sanchez@hotmail.com'),(SELECT id FROM tienda WHERE nombre='Lácteos y Huevos Los Andes'),  (SELECT id FROM estado_reserva WHERE nombre='Pendiente'),  'RES-0005', CURRENT_DATE + 2, NULL);

-- Detalle: 2 productos disponibles de cada tienda, con el precio de hoy
INSERT INTO detalle_reserva (id_reserva, id_producto, cantidad, precio_unitario)
SELECT r.id, i.id_producto, 25, v.precio
FROM reserva r
CROSS JOIN LATERAL (
  SELECT id_producto FROM inventario
  WHERE id_tienda = r.id_tienda AND cantidad_disponible >= 25
  ORDER BY id_producto LIMIT 2
) i
JOIN v_variacion_precio v ON v.id_producto = i.id_producto AND v.fecha = CURRENT_DATE;
