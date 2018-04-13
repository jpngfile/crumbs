import { h, app } from 'hyperapp'

const state = {
    file: ""
}
const actions = {
    setFile: value => state => ({file: value})
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
    </div>
)

app(state, actions, view, document.body)
