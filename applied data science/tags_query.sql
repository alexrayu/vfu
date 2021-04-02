SELECT n.nid, c.yearcount, COUNT(t.field_article_tags_target_id) FROM node n
LEFT OUTER JOIN node_counter c ON c.nid = n.nid
LEFT OUTER JOIN node__field_article_tags t ON t.entity_id = n.nid
WHERE n.type = "article"
GROUP BY n.nid
ORDER BY c.yearcount DESC; 
