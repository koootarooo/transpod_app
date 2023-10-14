import { defineStore } from 'pinia'


export const useMessageStore = defineStore('message', {
    state: () => ({
        message: "",
    }),
    actions: {
        let_login() {
            this.message = "この機能を利用するにはログインが必要です。"
        },
        delete_message() {
            this.message = ""
        }
    }
})