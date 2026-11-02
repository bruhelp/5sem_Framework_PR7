-- 1. Полный каталог произведений (выборка списка).
SELECT id, title, artist, year, image FROM paints ORDER BY year, title;

-- 2. Список коллекций (выборка списка).
SELECT id, name, description FROM collections ORDER BY name;

-- 3. Поиск произведений по автору (WHERE, параметр ?).
SELECT id, title, artist, year FROM paints
WHERE artist LIKE ? ORDER BY year;

-- 4. Поиск произведений в диапазоне лет (WHERE, BETWEEN).
SELECT id, title, artist, year FROM paints
WHERE year BETWEEN ? AND ? ORDER BY year;

-- 5. Произведения с названием коллекции (JOIN).
SELECT paints.id, paints.title, paints.artist, collections.name AS collection_name
FROM paints JOIN collections ON paints.collection_id = collections.id
ORDER BY paints.title;

-- 6. Карточка произведения с данными коллекции (JOIN).
SELECT paints.*, collections.name AS collection_name,
collections.description AS collection_description
FROM paints JOIN collections ON paints.collection_id = collections.id
WHERE paints.id = ?;

-- 7. Общее количество произведений (COUNT).
SELECT COUNT(*) AS paints_count FROM paints;

-- 8. Год создания самой ранней и поздней работы (MIN/MAX/AVG).
SELECT MIN(year) AS first_year, MAX(year) AS last_year,
AVG(year) AS average_year FROM paints;

-- 9. Количество произведений в каждой коллекции (GROUP BY, LEFT JOIN).
SELECT collections.id, collections.name, COUNT(paints.id) AS paints_count
FROM collections LEFT JOIN paints ON collections.id = paints.collection_id
GROUP BY collections.id, collections.name ORDER BY paints_count DESC;

-- 10. Количество произведений каждого художника (GROUP BY).
SELECT artist, COUNT(*) AS paints_count FROM paints
GROUP BY artist ORDER BY paints_count DESC, artist;

-- 11. Коллекции, содержащие больше указанного числа работ (HAVING).
SELECT collections.name, COUNT(paints.id) AS paints_count
FROM collections JOIN paints ON collections.id = paints.collection_id
GROUP BY collections.id, collections.name
HAVING COUNT(paints.id) > ? ORDER BY paints_count DESC;

-- 12. Каталог с ограничением выборки (LIMIT/OFFSET).
SELECT id, title, artist, year FROM paints
ORDER BY year, id LIMIT ? OFFSET ?;
