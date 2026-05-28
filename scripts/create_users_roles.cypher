//create users
create user neo4j_sa_full set password "password123" change not required;
create user neo4j_sa_limited set password "password123" change not required;
create user neo4j_sa_deidentified set password "password123" change not required;

//create roles
CREATE ROLE researcher_level1 AS COPY OF reader;
CREATE ROLE researcher_level2 AS COPY OF reader;
CREATE ROLE researcher_level3 AS COPY OF reader;

//assign users to roles
GRANT ROLE researcher_level1 TO neo4j_sa_full;
GRANT ROLE researcher_level2 TO neo4j_sa_limited;
GRANT ROLE researcher_level3 TO neo4j_sa_deidentified;

//add privleges - deny secondary labels for roles, so they can only traverse to their own (e.g. limited user can only see Limited, etc.)

DENY TRAVERSE ON GRAPH testthis NODES Full, Deidentified TO researcher_level2;
DENY TRAVERSE ON GRAPH testthis NODES Full, Limited TO researcher_level3;
