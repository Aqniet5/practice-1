-- =========================
-- PHONEBOOK PROJECT (P7 + P8)
-- =========================

-- 1. TABLE
DROP TABLE IF EXISTS phonebook;

CREATE TABLE phonebook (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(20) NOT NULL UNIQUE
);

-- =========================
-- PRACTICE 7 (BASIC CRUD)
-- =========================

-- Insert example
INSERT INTO phonebook(name, phone)
VALUES ('Ali', '87001234567');

-- Update example
UPDATE phonebook
SET phone = '7777777777'
WHERE name = 'Ali';

-- Delete example
-- DELETE FROM phonebook WHERE name = 'Ali';

-- =========================
-- PRACTICE 8
-- =========================

-- 2. SEARCH FUNCTION
CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE(id INT, name TEXT, phone TEXT)
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM phonebook
    WHERE name ILIKE '%' || pattern || '%'
       OR phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;


-- 3. UPSERT PROCEDURE
CREATE OR REPLACE PROCEDURE upsert_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


-- 4. INSERT MANY WITH VALIDATION
CREATE OR REPLACE PROCEDURE insert_many_users(
    names TEXT[],
    phones TEXT[],
    OUT invalid_data TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
    temp_invalid TEXT[] := ARRAY[]::TEXT[];
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP

        IF phones[i] ~ '^[0-9]{10,15}$' THEN

            IF EXISTS (SELECT 1 FROM phonebook WHERE name = names[i]) THEN
                UPDATE phonebook
                SET phone = phones[i]
                WHERE name = names[i];
            ELSE
                INSERT INTO phonebook(name, phone)
                VALUES (names[i], phones[i]);
            END IF;

        ELSE
            temp_invalid := array_append(temp_invalid,
                names[i] || ' -> ' || phones[i]);
        END IF;

    END LOOP;

    invalid_data := temp_invalid;
END;
$$;


-- 5. PAGINATION FUNCTION
CREATE OR REPLACE FUNCTION get_paginated(limit_val INT, offset_val INT)
RETURNS TABLE(id INT, name TEXT, phone TEXT)
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM phonebook
    ORDER BY id
    LIMIT limit_val OFFSET offset_val;
END;
$$ LANGUAGE plpgsql;


-- 6. DELETE PROCEDURE
CREATE OR REPLACE PROCEDURE delete_user(value TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = value OR phone = value;
END;
$$;