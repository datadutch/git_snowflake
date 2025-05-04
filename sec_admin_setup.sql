Use role securityadmin;

-- create role

Create role r_dev;
Grant usage, monitor on warehouse w_dev to role r_dev;
grant role r_dev to user SFBIDUTCH;

-- role grants
grant usage on database d_dev to role r_dev;
grant usage on schema d_Dev.s_Dev to role r_Dev;
grant create notebook on schema d_Dev.s_Dev to role r_Dev;
GRANT Read, write ON GIT REPOSITORY d_Dev.s_Dev.git_snowflake TO ROLE r_Dev;