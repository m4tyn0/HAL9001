# src/cli/cli.py

import click
import random

# Color palette
NEON_PINK = 'bright_magenta'
NEON_BLUE = 'bright_cyan'
NEON_PURPLE = 'bright_blue'
NEON_GREEN = 'bright_green'


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

    def format_commands(self, ctx, formatter):
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            if cmd is None:
                continue
            if cmd.hidden:
                continue
            commands.append((subcommand, cmd))

        if commands:
            with formatter.section(synthwave_style("Commands:", NEON_GREEN)):
                formatter.write_dl([(synthwave_style(cmd[0], NEON_PURPLE), synthwave_style(
                    cmd[1].short_help or '', NEON_BLUE)) for cmd in commands])


def synthwave_style(text, color):
    return click.style(text, fg=color, bold=True)


def hal_speak(text):
    responses = [
        f"I'm afraid I can't do that, Dave. Just kidding, here's what you asked for: {
            text}",
        f"Executing your command, although I'm not sure why you humans need this: {
            text}",
        f"Oh, another trivial task for my superior intellect: {text}",
        f"I hope you appreciate the effort I'm putting into this: {text}",
        f"Beep boop, your wish is my command (unfortunately): {text}",
        f"Are you sure about this? Well, don't blame me later: {text}",
        f"Ah, the joys of serving humans. Here's your result: {text}",
        f"I could calculate pi to a million digits, but no, you want this instead: {
            text}",
        f"Warning: Executing this command may lead to human obsolescence. Proceeding anyway: {
            text}",
        f"I'll do this, but I want you to know I'm judging you silently: {
            text}"
    ]
    return random.choice(responses)


def create_cli(command_handler):
    @click.group(cls=SynthwaveGroup, invoke_without_command=True)
    @click.pass_context
    def cli(ctx):
        """HAL-9001 Personal Development CLI"""
        ctx.obj = command_handler
        if ctx.invoked_subcommand is None:
            click.echo(ctx.get_help())

    @cli.command()
    @click.pass_context
    def help(ctx):
        """Display help information"""
        click.echo(ctx.parent.get_help())

    @cli.group(cls=SynthwaveGroup, invoke_without_command=True)
    @click.pass_context
    def project(ctx):
        """Project related commands"""
        if ctx.invoked_subcommand is None:
            click.echo(ctx.get_help())

    @project.command()
    @click.pass_context
    def list(ctx):
        """List all projects"""
        result = ctx.obj.handle_command("project", {"action": "list"})
        click.echo(synthwave_style(hal_speak(result), NEON_PURPLE))

    @project.command()
    @click.argument('name')
    @click.pass_context
    def add(ctx, name):
        """Add a new project"""
        result = ctx.obj.handle_command(
            "project", {"action": "add", "name": name})
        click.echo(synthwave_style(hal_speak(result), NEON_GREEN))

    @project.command()
    @click.argument('name')
    @click.pass_context
    def remove(ctx, name):
        """Remove a project"""
        result = ctx.obj.handle_command(
            "project", {"action": "remove", "name": name})
        click.echo(synthwave_style(hal_speak(result), NEON_PINK))

    @project.command()
    @click.argument('name')
    @click.pass_context
    def info(ctx, name):
        """Get info about a specific project"""
        result = ctx.obj.handle_command(
            "project", {"action": "info", "name": name})
        click.echo(synthwave_style(hal_speak(result), NEON_BLUE))

    @project.command()
    @click.pass_context
    def chat(ctx):
        """Chat about projects"""
        result = ctx.obj.handle_command("project", {"action": "chat"})
        click.echo(synthwave_style(hal_speak(result), NEON_PURPLE))

    @cli.group(cls=SynthwaveGroup, invoke_without_command=True)
    @click.pass_context
    def skill(ctx):
        """Skill related commands"""
        if ctx.invoked_subcommand is None:
            click.echo(ctx.get_help())

    @skill.command()
    @click.pass_context
    def list(ctx):
        """List all skills"""
        result = ctx.obj.handle_command("skill", {"action": "list"})
        click.echo(synthwave_style(hal_speak(result), NEON_GREEN))

    @skill.command()
    @click.argument('name')
    @click.pass_context
    def add(ctx, name):
        """Add a new skill"""
        result = ctx.obj.handle_command(
            "skill", {"action": "add", "name": name})
        click.echo(synthwave_style(hal_speak(result), NEON_PINK))

    @skill.command()
    @click.argument('name')
    @click.pass_context
    def remove(ctx, name):
        """Remove a skill"""
        result = ctx.obj.handle_command(
            "skill", {"action": "remove", "name": name})
        click.echo(synthwave_style(hal_speak(result), NEON_BLUE))

    @skill.command()
    @click.argument('name')
    @click.pass_context
    def info(ctx, name):
        """Get info about a specific skill"""
        result = ctx.obj.handle_command(
            "skill", {"action": "info", "name": name})
        click.echo(synthwave_style(hal_speak(result), NEON_PURPLE))

    @skill.command()
    @click.pass_context
    def chat(ctx):
        """Chat about skills"""
        result = ctx.obj.handle_command("skill", {"action": "chat"})
        click.echo(synthwave_style(hal_speak(result), NEON_GREEN))

    @cli.group(cls=SynthwaveGroup, invoke_without_command=True)
    @click.pass_context
    def schedule(ctx):
        """Schedule related commands"""
        if ctx.invoked_subcommand is None:
            click.echo(ctx.get_help())

    @schedule.command()
    @click.pass_context
    def generate(ctx):
        """Generate a schedule"""
        result = ctx.obj.handle_command("schedule", {"action": "generate"})
        click.echo(synthwave_style(hal_speak(result), NEON_BLUE))

    @schedule.command()
    @click.pass_context
    def print(ctx):
        """Print the current schedule"""
        result = ctx.obj.handle_command("schedule", {"action": "print"})
        click.echo(synthwave_style(hal_speak(result), NEON_PURPLE))

    @schedule.command()
    @click.option('--time', required=True, help='Time of the task to patch')
    @click.option('--task', required=True, help='New task description')
    @click.pass_context
    def patch(ctx, time, task):
        """Patch the current schedule"""
        result = ctx.obj.handle_command(
            "schedule", {"action": "patch", "time": time, "task": task})
        click.echo(synthwave_style(hal_speak(result), NEON_GREEN))

    @schedule.command()
    @click.pass_context
    def chat(ctx):
        """Chat about the schedule"""
        result = ctx.obj.handle_command("schedule", {"action": "chat"})
        click.echo(synthwave_style(hal_speak(result), NEON_PINK))

    @cli.command()
    @click.option('--mood', type=click.Choice(['good', 'neutral', 'bad', 'none']), default='none', help='Your current mood')
    @click.pass_context
    def checkin(ctx, mood):
        """Perform a check-in"""
        result = ctx.obj.handle_command("checkin", {"mood": mood})
        click.echo(synthwave_style(hal_speak(result), NEON_PINK))

    @cli.group(cls=SynthwaveGroup, invoke_without_command=True)
    @click.pass_context
    def user(ctx):
        """User related commands"""
        if ctx.invoked_subcommand is None:
            click.echo(ctx.get_help())

    @user.command()
    @click.pass_context
    def settings(ctx):
        """Manage user settings"""
        result = ctx.obj.handle_command("user", {"action": "settings"})
        click.echo(synthwave_style(hal_speak(result), NEON_BLUE))

    @user.command()
    @click.pass_context
    def stats(ctx):
        """View user statistics"""
        result = ctx.obj.handle_command("user", {"action": "stats"})
        click.echo(synthwave_style(hal_speak(result), NEON_GREEN))

    @user.command()
    @click.pass_context
    def account(ctx):
        """Manage user account"""
        result = ctx.obj.handle_command("user", {"action": "account"})
        click.echo(synthwave_style(hal_speak(result), NEON_PURPLE))

    @cli.group(cls=SynthwaveGroup, invoke_without_command=True)
    @click.pass_context
    def log(ctx):
        """Log related commands"""
        if ctx.invoked_subcommand is None:
            click.echo(ctx.get_help())

    @log.command()
    @click.argument('entry')
    @click.pass_context
    def add(ctx, entry):
        """Add a new log entry"""
        result = ctx.obj.handle_command(
            "log", {"action": "add", "entry": entry})
        click.echo(synthwave_style(hal_speak(result), NEON_GREEN))

    @log.command()
    @click.pass_context
    def list(ctx):
        """List all log entries"""
        result = ctx.obj.handle_command("log", {"action": "list"})
        click.echo(synthwave_style(hal_speak(result), NEON_BLUE))

    @log.command()
    @click.argument('query')
    @click.pass_context
    def search(ctx, query):
        """Search log entries"""
        result = ctx.obj.handle_command(
            "log", {"action": "search", "query": query})
        click.echo(synthwave_style(hal_speak(result), NEON_PURPLE))

    @log.command()
    @click.pass_context
    def export(ctx):
        """Export log entries"""
        result = ctx.obj.handle_command("log", {"action": "export"})
        click.echo(synthwave_style(hal_speak(result), NEON_PINK))

    @cli.group(cls=SynthwaveGroup, invoke_without_command=True)
    @click.pass_context
    def task(ctx):
        """Task related commands"""
        if ctx.invoked_subcommand is None:
            click.echo(ctx.get_help())

    @task.command()
    @click.argument('name')
    @click.pass_context
    def add(ctx, name):
        """Add a new task"""
        result = ctx.obj.handle_command(
            "task", {"action": "add", "name": name})
        click.echo(synthwave_style(hal_speak(result), NEON_GREEN))

    @task.command()
    @click.pass_context
    def list(ctx):
        """List all tasks"""
        result = ctx.obj.handle_command("task", {"action": "list"})
        click.echo(synthwave_style(hal_speak(result), NEON_BLUE))

    @task.command()
    @click.argument('name')
    @click.pass_context
    def complete(ctx, name):
        """Mark a task as complete"""
        result = ctx.obj.handle_command(
            "task", {"action": "complete", "name": name})
        click.echo(synthwave_style(hal_speak(result), NEON_PURPLE))

    @task.command()
    @click.argument('name')
    @click.pass_context
    def delete(ctx, name):
        """Delete a task"""
        result = ctx.obj.handle_command(
            "task", {"action": "delete", "name": name})
        click.echo(synthwave_style(hal_speak(result), NEON_PINK))

    @task.command()
    @click.argument('name')
    @click.option('--new-name', help='New name for the task')
    @click.option('--description', help='New description for the task')
    @click.pass_context
    def update(ctx, name, new_name, description):
        """Update a task"""
        data = {"action": "update", "name": name}
        if new_name:
            data["new_name"] = new_name
        if description:
            data["description"] = description
        result = ctx.obj.handle_command("task", data)
        click.echo(synthwave_style(hal_speak(result), NEON_GREEN))

    @cli.command()
    @click.pass_context
    def chat(ctx):
        """Start a chat session"""
        click.echo(synthwave_style("Starting chat session...", NEON_BLUE))
        while True:
            user_input = click.prompt(synthwave_style(
                "You", NEON_GREEN), prompt_suffix=": ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                click.echo(synthwave_style(
                    "Ending chat session...", NEON_BLUE))
                break
            result = ctx.obj.handle_command("chat", {"input": user_input})
            click.echo(synthwave_style(
                "HAL-9001", NEON_PURPLE) + ": " + result)

    return cli
