window.toastHandler = function() {
	return {
		messages: [],
		visible: [],
		add(toast) {
			toast.id = Date.now()
			this.messages.push(toast)
			this.fire(toast.id)
		},
		fire(id) {
			this.visible.push(this.messages.find(toast => toast.id == id))
			const timeShown = 2000 * this.visible.length
			setTimeout(() => {
				this.remove(id)
			}, timeShown)
		},
		remove(id) {
			const toast = this.visible.find(toast => toast.id == id)
			const index = this.visible.indexOf(toast)
			this.visible.splice(index, 1)
		},
		
	};
}
