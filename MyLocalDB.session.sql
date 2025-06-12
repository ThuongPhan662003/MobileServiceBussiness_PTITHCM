
-- CREATE PROCEDURE sp_get_functions_by_rolegroup_id (
--     IN p_rolegroup_id INT
-- )
-- BEGIN
--     SELECT 
--         f.id,
--         f.function_name,
--         f.syntax_name
--     FROM rolegroupdetail rgd
--     JOIN functions f ON rgd.function_id = f.id
--     WHERE rgd.role_group_id = p_rolegroup_id;
-- END;
call 
