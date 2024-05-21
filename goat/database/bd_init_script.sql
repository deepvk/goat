create table if not exists public.leaderboard
(
    model varchar not null
        primary key,
    single_choice double precision,
    multiple_choice double precision,
    word_gen double precision
);

alter table public.leaderboard
    owner to habrpguser;

create table if not exists public.eval_requests
(
    id          serial
        constraint eval_requests_pk
            primary key,
    model_name  varchar not null,
    precision   varchar not null
);

alter table public.eval_requests
    owner to habrpguser;

alter table public.eval_requests
    owner to habrpguser;

create or replace function notify_id_trigger()
returns trigger as $$
begin
    perform pg_notify('id'::text, NEW."id"::text);
    return new;
end;
$$ language plpgsql;

create trigger trigger1
after insert or update on public."eval_requests"
for each row execute procedure notify_id_trigger();
