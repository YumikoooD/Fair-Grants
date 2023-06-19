CREATE DATABASE IF NOT EXISTS graph;
USE graph;

DROP TABLE IF EXISTS votes;
DROP TABLE IF EXISTS contributions;

CREATE TABLE votes (
    id VARCHAR(255) primary key,
    transactionHash text,
    blockNumber int,
    blockTimestamp datetime default current_timestamp not null,
    projectId text,
    applicationIndex int,
    roundAddress text,
    voter text,
    grantAddress text,
    token text,
    amount decimal(40),
    amountUsd decimal(40, 4)
);

CREATE TABLE contributions (
    id VARCHAR(255) primary key,
    projectId text,
    walletId text,
    amountContributedUsd decimal(19, 4),
    createdAt datetime default current_timestamp not null,
    updatedAt datetime default current_timestamp not null
);

