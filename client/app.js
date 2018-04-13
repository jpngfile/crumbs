import { h, app } from 'hyperapp'
import { location, Route } from '@hyperapp/router'
import { withFx, http } from '@hyperapp/fx'

const state = {
    board: {
        team: '',
        headers: {}
    },
    location: location.state
}

const actions = {
    getTeam: team => http(
        `http://localhost:5000/api/${team}`,
        'setBoard'
    ),
    setBoard: board => ({ board }),
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

const App = ({ location, match }) => {
    actions.getTeam(match.params.team)
    console.log(state)

    return (
        <Board team={state.board.team} headers={state.board.headers} />
    )
}

const view = (state, actions) => (
    <div>
        <h1>Upload a scrum board picture!</h1>
        <form>
            <input type="file" name="file" accept="image/*" capture /><br />
            <input type="text" name="team" placeholder="Team name!" />
            <input type="submit" value="Scrum!" />
        </form>

        <Route path="/board/:team" render={App} />
    </div>
)

const main = withFx(app)(state, actions, view, document.body)
const unsubscribe = location.subscribe(main.location)
