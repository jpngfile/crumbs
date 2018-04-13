import { h, app } from 'hyperapp'

const state = {}
const actions = {}

const view = (state, actions) => (
    <div className="front-page">
        <h1>Upload a scrum board picture!</h1>
        <form>
            <input type="file" name="file" accept="image/*" capture /><br />
            <input type="text" name="team" placeholder="Team name!" />
            <input type="submit" value="Scrum!" />
        </form>
    </div>
)

app(state, actions, view, document.body)
