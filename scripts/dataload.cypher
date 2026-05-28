//create persons - mock data
CREATE (p1:Person {id: "123"})
CREATE (p2:Person {id: "234"})
CREATE (p3:Person {id: "345"})

//create PersonAttributes and assign transformed/non-transformed values, as per the secondary label 
CREATE (a1:PersonAttributes:Deidentified {dob: "XX-XX-XXXX", ssn: "XXX-XX-XXXX", name: "Test Patient 1"})
CREATE (a2:PersonAttributes:Limited {dob: "02/02/2001", ssn: "XXX-XX-XXXX", name: "Test Patient 1"})
CREATE (a3:PersonAttributes:Full {dob: "02/02/2001", ssn: "111-11-1111", name: "Test Patient 1"})

CREATE (a4:PersonAttributes:Deidentified {dob: "XX-XX-XXXX", ssn: "XXX-XX-XXXX", name: "Test Patient 2"})
CREATE (a5:PersonAttributes:Limited {dob: "02/02/2002", ssn: "XXX-XX-XXXX", name: "Test Patient 2"})
CREATE (a6:PersonAttributes:Full {dob: "02/02/2002", ssn: "111-11-1112", name: "Test Patient 2"})

CREATE (a7:PersonAttributes:Deidentified {dob: "XX-XX-XXXX", ssn: "XXX-XX-XXXX", name: "Test Patient 3"})
CREATE (a8:PersonAttributes:Limited {dob: "02/02/2003", ssn: "XXX-XX-XXXX", name: "Test Patient 3"})
CREATE (a9:PersonAttributes:Full {dob: "02/02/2003", ssn: "111-11-1113"})


//assign attributes to person
CREATE (p1)-[:HAS_PERSON_ATTRIBUTES]->(a1)
CREATE (p1)-[:HAS_PERSON_ATTRIBUTES]->(a2)
CREATE (p1)-[:HAS_PERSON_ATTRIBUTES]->(a3)

CREATE (p2)-[:HAS_PERSON_ATTRIBUTES]->(a4)
CREATE (p2)-[:HAS_PERSON_ATTRIBUTES]->(a5)
CREATE (p2)-[:HAS_PERSON_ATTRIBUTES]->(a6)

CREATE (p3)-[:HAS_PERSON_ATTRIBUTES]->(a7)
CREATE (p3)-[:HAS_PERSON_ATTRIBUTES]->(a8)
CREATE (p3)-[:HAS_PERSON_ATTRIBUTES]->(a9)
