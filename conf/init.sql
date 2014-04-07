create database mobile;
use mobile;

create table user(
    uid bigint unsigned not null primary key auto_increment,
    username char(20) ,
    password char(20) ,
    chiname char(20),
    locid integer,
    imagesample char(100),
    audioengine char(100),
    createtime datetime,
    department char(100)
    );
alter table user add unique(username);
alter table user modify chiname char(20) character set gbk;
alter table user modify department char(20) character set gbk;

create table administrator(
    uid bigint unsigned not null primary key auto_increment,
    username char(20),
    chiname char(20),
    password char(20)
);
alter table administrator add unique(username);
alter table administrator modify chiname char(20) character set gbk;
insert into administrator(username,password) values('admin','admin');
alter table administrator add constraint
    chk_admin check (10 >= (select count(*) from administrator));

create table audio(
    owner bigint unsigned not null,
    foreign key(owner) references user(uid) on delete cascade on update cascade,
    audiohash char(100) primary key,
    createtime datetime
);

create table location(
    locid integer unsigned not null primary key auto_increment,
    locationname char(100),
    longitude double,
    latitude double,
    starttime datetime,
    termitime datetime
);
alter table location modify locationname char(100) character set gbk;
insert into location(locid,locationname,longitude,latitude) values(1,'sjtu',121.43574714660645,31.024988336871534);

create table detect(
    owner bigint unsigned not null,
    foreign key(owner) references user(uid) on delete cascade on update cascade,
    sessionid bigint unsigned not null primary key auto_increment,
    audiohash char(100),
    audiodetect double,
    longitude double,
    latitude double,
    facehash char(100),
    facedetect float,
    detecttime datetime,
    status bool
);
