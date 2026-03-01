CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary DECIMAL(10,2) NOT NULL,
    hire_date DATE NOT NULL DEFAULT CURRENT_DATE
);

INSERT INTO employees (name, position, department, salary, hire_date) VALUES
('Alejandro Morales', 'Socio Senior', 'Litigios', 120000, '2010-03-15'),
('Isabel Fernández', 'Abogada Asociada', 'Derecho Corporativo', 85000, '2015-07-01'),
('Roberto Castillo', 'Socio Fundador', 'Derecho Penal', 150000, '2005-01-10'),
('Valentina Torres', 'Abogada Junior', 'Derecho Laboral', 55000, '2022-08-20'),
('Diego Ramírez', 'Paralegal Senior', 'Litigios', 45000, '2018-04-12'),
('Sofía Herrera', 'Abogada Asociada', 'Derecho Inmobiliario', 80000, '2017-09-05'),
('Andrés Vargas', 'Director Legal', 'Compliance', 110000, '2012-11-30'),
('Camila Jiménez', 'Abogada Junior', 'Derecho Corporativo', 52000, '2023-02-14'),
('Luis Mendoza', 'Paralegal', 'Derecho Laboral', 38000, '2021-06-07'),
('Patricia Núñez', 'Secretaria Legal', 'Administración', 32000, '2019-10-22');
