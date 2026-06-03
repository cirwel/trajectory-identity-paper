-- Resident-discrimination pilot: pull real (non-synthetic) EISV+phi time-series
-- for the four dense resident agents over the last 60 days.
-- Regenerates experiments/resident-discrimination/resident_states.csv (gitignored;
-- raw production state rows are not committed to this public repo).
--
--   psql governance -f fetch.sql
\copy (select s.identity_id, a.label as agent, s.recorded_at, \
       (s.state_json->>'E')::float as e, s.integrity as i, s.entropy as s, \
       s.volatility as v, (s.state_json->>'phi')::float as phi, \
       s.risk_score, s.regime \
       from core.agent_state s \
       join core.identities i on i.identity_id = s.identity_id \
       join core.agents a on a.id = i.agent_id \
       where s.synthetic is not true \
         and s.recorded_at > now() - interval '60 days' \
         and s.identity_id in (2522,3701,6951,3696) \
       order by s.identity_id, s.recorded_at) \
  to 'resident_states.csv' csv header
