import click


def validate_k(ctx, param, value):
    if 0.0 <= value and value <= 1.0:
        return value
    raise click.BadParameter('The value of k must be between 0 and 1')
