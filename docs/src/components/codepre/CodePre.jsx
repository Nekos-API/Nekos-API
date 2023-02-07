import { Pre } from 'nextra/components';

import styles from './CodePre.module.css';

export default function CodePre({
    children,
    language,
}) {
    const hljs = require('highlight.js');

    return (
        <Pre>
            <div 
                dangerouslySetInnerHTML={{ __html: hljs.highlight(children, { language }).value }}
                className={styles.container}></div>
        </Pre>
    )
}