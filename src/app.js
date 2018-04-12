import { h, app } from 'hyperapp'

const state = {}
const actions = {}

const view = (state, actions) => (
    <div>
        <h1>Take a picture</h1>
        <form>
            <input type='file' accept="image/*" capture></input>
            <input type="submit" value="Upload"></input>
        </form>
    </div>
)

app(state, actions, view, document.body)
