-- SQLite
create table user (
    UserID int(5) primary key,
    Name varchar(40)
);

create table drinks (
    DrinkID int(5) primary key,
    Name varchar(40),
    price float(4),
);

create table entry (
    ID int(5) primary key,
    UserID int(5),
    DrinkID int(5),
    Date date,
    Time CURRENT_TIME
);