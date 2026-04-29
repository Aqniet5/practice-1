CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)

LANGUAGE plpgsql AS $$

DECLARE

    v_contact_id INT;

BEGIN

    SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;

    IF v_contact_id IS NOT NULL THEN

        INSERT INTO phones (contact_id, phone, type) VALUES (v_contact_id, p_phone, p_type);

    ELSE

        RAISE NOTICE 'Contact % not found.', p_contact_name;

    END IF;

END;

$$;

-- 2. Procedure to move contact to a group
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INT;
BEGIN
    -- Create group if it doesn't exist
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    
    UPDATE contacts SET group_id = v_group_id WHERE name = p_contact_name;
END;
$$;

-- 3. Advanced Search Function (Matches everything)
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(contact_name VARCHAR, email VARCHAR, phone_list TEXT, group_name VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.name, c.email, STRING_AGG(p.phone || ' (' || p.type || ')', ', '), g.name
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    LEFT JOIN groups g ON c.group_id = g.id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name;
END;
$$ LANGUAGE plpgsql;