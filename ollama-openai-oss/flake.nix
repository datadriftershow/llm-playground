{
  description = "A flake for an Ollama chat REPL";

  # Define the inputs for the flake, pinning versions for reproducibility.
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  # Define the outputs of the flake.
  outputs = { self, nixpkgs, flake-utils, ... }:
    # Use flake-utils to generate outputs for common systems (x86_64-linux, aarch64-linux, etc.)
    flake-utils.lib.eachDefaultSystem (system:
      let
        # Import the nixpkgs set for the specific system.
        pkgs = import nixpkgs {
          inherit system;
          # Ollama may depend on unfree packages like NVIDIA drivers.
          config.allowUnfree = true;
        };

        # Create a specific Python environment with the 'requests' library.
        # This is more efficient than adding 'requests' to the global packages.
        pythonEnv = pkgs.python3.withPackages (ps: [
          ps.requests
        ]);

      in
      {
        # --- Development Environment ---
        # Accessed via `nix develop`
        devShells.default = pkgs.mkShell {
          name = "ollama-chat-shell";

          # List of packages available in the shell.
          packages = [
            pythonEnv    # Provides `python` and the `requests` library.
            pkgs.ollama  # Includes the ollama CLI for managing the server.
            pkgs.glow    # Adds the glow markdown renderer.
          ];

          # A hook to print instructions when the shell is entered.
          shellHook = ''
            echo "✅ Entered the Ollama Chat development shell."
            echo "   Run the client with: python chat.py"
            echo "   Manage the server with the 'ollama' command (e.g., 'ollama list')."
          '';
        };

        # --- Runnable Application ---
        # Executed via `nix run`
        apps.default = {
          type = "app";
          # The program to run is the Python interpreter from our custom environment,
          # with the chat.py script as the argument.
          program = "${pythonEnv}/bin/python ${./chat.py}";
        };
      });
}
