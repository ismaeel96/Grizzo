
CREATE TABLE Grizzo (
                ID VARCHAR(50) NOT NULL,
                PRIMARY KEY (ID)
);


CREATE TABLE Words (
                ID VARCHAR(50) NOT NULL,
                word VARCHAR(255),
                PRIMARY KEY (ID)
);


ALTER TABLE Words ADD CONSTRAINT grizzo_words_fk
FOREIGN KEY (ID)
REFERENCES Grizzo (ID)
ON DELETE NO ACTION
ON UPDATE NO ACTION;