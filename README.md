# SanEnv

# :m

CREATE TABLE parent (
  parent_id integer primary key,
  ...
);

CREATE TABLE child (
  child_id integer primary key,
  parent_id integer not null references parent(parent_id),
  ...
);

# m:n:

CREATE TABLE m(
   m_id integer primary key,
   ...
);

CREATE TABLE n(
   n_id integer primary key,
   ...
);

CREATE TABLE m_n (
   m_id integer references m(m_id),
   n_id integer references n(n_id),
   PRIMARY KEY(m_id, n_id),
   ...
);

# IF SWITCHSHOW
(?=switchshow:)switchshow|(?=switchshow\s)switchshow

# END
^(?=real)real