import { h, app } from 'hyperapp'
import { location, Route } from '@hyperapp/router'

const state = {
    file: "",
    board: {
        team: 'not loaded',
        headers: {
            test: ['string', 'aaa']
        }
    },
    location: location.state
}

const actions = {
    setFile: value => state => ({file: value}),
    getTeam: async (team) => {
        const payload = await fetch(`http://localhost:5000/api/${team}`)
        const board = await payload.json()
        actions.setBoard(board)
    },
    setBoard: board => ({ board: 5 }),
    location: location.actions
}

const Sticky = ({ content }) => (
    <li>{content}</li>
)

const Header = ({ header, stickies }) => (
    <div>
        <h3>{header}</h3>
        <ul>
            {stickies.map((sticky) => (
            <Sticky content={sticky} />
            ))}
        </ul>
    </div>
)

const Board = ({ team, headers }) => (
    <div>
        <h1>{team}</h1>
        <div>
            {Object.keys(headers).map((key) => (
            <Header header={key} stickies={headers[key]} />
            ))}
        </div>
    </div>
)

const App = (state, actions) => ({ location, match }) => {
    actions.getTeam(match.params.team)

    return (
        <Board team={state.board.team} headers={state.board.headers} />
    )
}

const view = (state, actions) => (
    <div className="front-page">
        <h1>Upload a scrum board picture!</h1>
        <form>
            <label className="btn file-label" for="file-upload"> Custom Upload </label>
            <span className="file-name" id="file-selected">{state.file}</span>
            <input id="file-upload" onchange={() => {
                var fileName = document.getElementById('file-upload').value
                var basename = fileName.split('\\').reverse()[0]
                if (basename){
                    actions.setFile(basename)
                }
            }} type="file" name="file" accept="image/*" capture /><br />

            <label for="team-name">Team name</label>
            <input id="team-name" type="text" name="team" placeholder="Team name!" />
            <input className="btn" type="submit" value="Scrum!" />
        </form>

        <Route path="/board/:team" state={state} actions={actions} render={App(state, actions)} />
    </div>
)

const main = app(state, actions, view, document.body)
const unsubscribe = location.subscribe(main.location)
