import click
from typing import Dict, Any
from engine.command_handler import CommandHandler

NEON_PINK = 'bright_magenta'
NEON_BLUE = 'bright_cyan'
NEON_PURPLE = 'bright_blue'
NEON_GREEN = 'bright_green'
NEON_YELLOW = 'bright_yellow'


class SynthwaveGroup(click.Group):
    def format_help(self, ctx, formatter):
        formatter.write(synthwave_style(
            self.get_short_help_str() + "\n", NEON_BLUE))
        formatter.write(synthwave_style(
            "Usage: " + ctx.command_path + " [OPTIONS] COMMAND [ARGS]...\n", NEON_GREEN))
        self.format_options(ctx, formatter)
        self.format_commands(ctx, formatter)

    def format_options(self, ctx, formatter):
        opts = []
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None:
                opts.append(rv)

        if opts:
            with formatter.section(synthwave_style("Options:", NEON_GREEN)):
                formatter.write_dl([(synthwave_style(opt[0], NEON_PURPLE), synthwave_style(
                    opt[1], NEON_BLUE)) for opt in opts])


def synthwave_style(text, color):
    return click.style(text, fg=color, bold=True)


def create_cli(command_handler: CommandHandler):
    @click.group(cls=SynthwaveGroup, invoke_without_command=True)
    @click.pass_context
    def cli(ctx):
        """HAL-9001 Personal Development CLI"""
        ctx.obj = command_handler
        if ctx.invoked_subcommand is None:
            click.echo(ctx.get_help())

    @cli.command()
    @click.pass_context
    def chat(ctx):
        """Start a chat session"""
        click.echo(synthwave_style("Starting chat session...", NEON_BLUE))
        click.echo(synthwave_style(
            "Type 'exit' to end the session, or 'help' for available commands.", NEON_YELLOW))
        while True:
            user_input = click.prompt(synthwave_style(
                "You", NEON_GREEN), prompt_suffix=": ")
            if user_input.lower() == 'exit':
                click.echo(synthwave_style(
                    "Ending chat session...", NEON_BLUE))
                break
            elif user_input.lower() in ['history', 'clear', 'help']:
                result = ctx.obj.handle_command(user_input.lower())
                click.echo(synthwave_style(result, NEON_YELLOW))
            else:
                result = ctx.obj.handle_chat(user_input)
                click.echo(synthwave_style(f"HAL-9001: {result}", NEON_PURPLE))

    @cli.command()
    @click.pass_context
    def onboard(ctx):
        """Start the onboarding process"""
        click.echo(synthwave_style("Starting onboarding process...", NEON_BLUE))
        while True:
            user_input = click.prompt(synthwave_style(
                "You", NEON_GREEN), prompt_suffix=": ")
            if user_input.lower() == 'exit':
                click.echo(synthwave_style(
                    "Ending chat session...", NEON_BLUE))
                break
            elif user_input.lower() in ['history', 'clear', 'help']:
                result = ctx.obj.handle_command(user_input.lower())
                click.echo(synthwave_style(result, NEON_YELLOW))
            else:
                result = ctx.obj.handle_onboarding(user_input)
                click.echo(synthwave_style(f"HAL-9001: {result}", NEON_PURPLE))

    @cli.command()
    @click.pass_context
    def history(ctx):
        """Show conversation history"""
        result = ctx.obj.handle_command('history')
        click.echo(synthwave_style(result, NEON_YELLOW))

    @cli.command()
    @click.pass_context
    def clear(ctx):
        """Clear conversation history"""
        result = ctx.obj.handle_command('clear')
        click.echo(synthwave_style(result, NEON_YELLOW))

    @cli.group()
    def skill():
        """Manage skills"""
        pass

    @skill.command('add')
    @click.pass_context
    def add_skill(ctx):
        """Add a new skill"""
        name = click.prompt(synthwave_style("Skill name", NEON_GREEN))
        description = click.prompt(synthwave_style("Description", NEON_GREEN))
        xp = click.prompt(synthwave_style(
            "Initial XP", NEON_GREEN), type=int, default=0)
        result = ctx.obj.handle_command(
            'add_skill', name=name, description=description, xp=xp)
        click.echo(synthwave_style(result, NEON_YELLOW))

    @skill.command('list')
    @click.pass_context
    def list_skills(ctx):
        """List all skills"""
        result = ctx.obj.handle_command('list_skills')
        click.echo(result)

    @cli.group()
    def project():
        """Manage projects"""
        pass

    @project.command('add')
    @click.pass_context
    def add_project(ctx):
        """Add a new project"""
        name = click.prompt(synthwave_style("Project name", NEON_GREEN))
        description = click.prompt(synthwave_style("Description", NEON_GREEN))
        status = click.prompt(synthwave_style(
            "Status", NEON_GREEN), default="Not Started")
        priority = click.prompt(synthwave_style(
            "Priority", NEON_GREEN), type=int)
        estimated_duration = click.prompt(synthwave_style(
            "Estimated duration (days)", NEON_GREEN), type=int)
        xp_amount = click.prompt(synthwave_style(
            "XP amount", NEON_GREEN), type=int)
        tags = click.prompt(synthwave_style(
            "Tags (comma-separated)", NEON_GREEN)).split(',')
        result = ctx.obj.handle_command('add_project', name=name, description=description, status=status,
                                        priority=priority, estimated_duration=estimated_duration,
                                        xp_amount=xp_amount, tags=tags)
        click.echo(synthwave_style(result, NEON_YELLOW))

    @project.command('list')
    @click.pass_context
    def list_projects(ctx):
        """List all projects"""
        result = ctx.obj.handle_command('list_projects')
        click.echo(result)

    @cli.group()
    def task():
        """Manage tasks"""
        pass

    @task.command('add')
    @click.pass_context
    def add_task(ctx):
        """Add a new task"""
        name = click.prompt(synthwave_style("Task name", NEON_GREEN))
        description = click.prompt(synthwave_style("Description", NEON_GREEN))
        status = click.prompt(synthwave_style(
            "Status", NEON_GREEN), default="Not Started")
        xp_amount = click.prompt(synthwave_style(
            "XP amount", NEON_GREEN), type=int)
        duration = click.prompt(synthwave_style(
            "Duration (minutes)", NEON_GREEN), type=int)
        task_type = click.prompt(synthwave_style("Type", NEON_GREEN), type=click.Choice(
            ['one-time', 'recurring', 'habit', 'routine']))
        priority = click.prompt(synthwave_style(
            "Priority", NEON_GREEN), type=int)
        due_date = click.prompt(synthwave_style(
            "Due date (YYYY-MM-DD)", NEON_GREEN))
        difficulty = click.prompt(synthwave_style(
            "Difficulty (1-5)", NEON_GREEN), type=click.IntRange(1, 5))
        energy_required = click.prompt(synthwave_style(
            "Energy required (1-5)", NEON_GREEN), type=click.IntRange(1, 5))
        tags = click.prompt(synthwave_style(
            "Tags (comma-separated)", NEON_GREEN)).split(',')
        result = ctx.obj.handle_command('add_task', name=name, description=description, status=status,
                                        xp_amount=xp_amount, duration=duration, task_type=task_type,
                                        priority=priority, due_date=due_date, difficulty=difficulty,
                                        energy_required=energy_required, tags=tags)
        click.echo(synthwave_style(result, NEON_YELLOW))

    @task.command('list')
    @click.pass_context
    def list_tasks(ctx):
        """List all tasks"""
        result = ctx.obj.handle_command('list_tasks')
        click.echo(result)

    return cli
