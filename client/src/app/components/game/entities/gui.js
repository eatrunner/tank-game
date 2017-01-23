angular
	.module('app.components.game.entities')
	.factory('Gui', function(GameState, gameService) {
		function Gui(game, gameInfo, gameState) {
			this._game = game;
			this._running = false;

			gameState.onUpdate.add(this._update, this);

    		this._spaceKey = game.input.keyboard.addKey(Phaser.Keyboard.SPACEBAR);
    		this._cursorKeys = game.input.keyboard.createCursorKeys();

    		this._spaceKey.onDown.add(this._shoot, this);
    		this._cursorKeys.up.onDown.add(this._movePlayer, this, null, "up");
    		this._cursorKeys.down.onDown.add(this._movePlayer, this, null, "down");
    		this._cursorKeys.right.onDown.add(this._movePlayer, this, null, "right");
    		this._cursorKeys.left.onDown.add(this._movePlayer, this, null, "left");
		}

		Gui.prototype._update = function(gameStateData) {
			if(gameStateData.status === GameState.Statuses.RUN) {
				this._running = true;
			} else {
				this._running = false;
			}
		};

		Gui.prototype._movePlayer = function(key, direction) {
			if(!this._running)
				return;

			gameService
				.movePlayer(direction)
				.then(movePlayerCallback, movePlayerError);

			var self = this;
			function movePlayerCallback(response) {
				if(response.error)
					$log.warn(response.error);
			}

			function movePlayerError(reason) {
				$log.error(reason);
			}
		};

		Gui.prototype._shoot = function(key) {
			if(!this._running)
				return;

			gameService
				.playerShoot(this.id)
				.then(playerShootCallback, playerShootError);

			var self = this;
			function playerShootCallback(response) {
				if(response.error)
					$log.warn(response.error);
				self._sendingShoot = false;
			}

			function playerShootError(reason) {
				$log.error(reason);
				self._sendingShoot = false;
			}
		};

		return Gui;
	});