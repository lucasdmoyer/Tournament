
create Table players(
	id serial primary key,
	name text
);

create Table matches(
	matchid serial primary key,
	winid serial references players (id),
	loseid serial references players (id)
);

create view totals as select players.id, count(matchid) as total from players left join matches on (players.id = matches.winid) or (players.id = matches.loseid) group by players.id;

create view wins as select players.id, count(matches.winid) as wins from players left join matches on players.id = matches.winid group by players.id order by wins desc;

create view winsandtotals as select totals.id, wins.wins, totals.total from totals join wins on totals.id = wins.id;

create view standings as select players.id, players.name, winsandtotals.wins, winsandtotals.total from players left join winsandtotals on players.id = winsandtotals.id group by winsandtotals.wins, players.id, winsandtotals.total order by wins desc;

create view standingseven as select t.* from (select *, row_number() over(order by wins desc) as row from standings) t where t.row % 2 = 0;

create view standingsodd as select t.* from (select *, row_number() over(order by wins desc) as row from standings) t where t.row % 2 != 0;
