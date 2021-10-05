## Status

Ready for review / Work in progress

## Description of Changes

Fixes #.

Changes proposed in this pull request:

## Testing

How should the reviewer test this PR?
Write out any special testing steps here.

## Deployment

Any special considerations for deployment? Consider both:

1. Upgrading existing production instances.
2. New installs.

## Checklist

### If you made changes to the server application code:

- [ ] Linting (`make lint`) and tests (`make test`) pass in the development container

### If you made changes to `securedrop-admin`:

- [ ] Linting and tests (`make -C admin test`) pass in the admin development container

### If you made changes to the system configuration:

- [ ] [Configuration tests](https://docs.securedrop.org/en/latest/development/testing_configuration_tests.html) pass

### If you added or removed a file deployed with the application:

- [ ] I have updated AppArmor rules to include the change

### If you made non-trivial code changes:

- [ ] I have written a test plan and validated it for this PR

Choose one of the following:

- [ ] I have opened a PR in the [docs repo](https://github.com/freedomofpress/securedrop-docs) for these changes, or will do so later
- [ ] I would appreciate help with the documentation
- [ ] These changes do not require documentation

### If you added or updated a production code dependency:

Production code dependencies are defined in:

- `admin/requirements.in`
- `admin/requirements-ansible.in`
- `securedrop/requirements/python3/securedrop-app-code-requirements.in`

If you changed another `requirements.in` file that applies only to development
or testing environments, then no diff review is required, and you can skip
(remove) this section.

Choose one of the following:

- [ ] I have performed a diff review and pasted the contents to [the packaging wiki](https://github.com/freedomofpress/securedrop-debian-packaging/wiki)
- [ ] I would like someone else to do the diff review
