import { useEffect, useRef, useState } from "react";

import { AnimatePresence, motion, domAnimation } from "framer-motion"

import styles from "./index.module.css"

function getPopupAlignmentUtilityClass(alignment) {
    /* Returns the alignment utility class name depending on the alignment provided */
    switch (alignment) {
        case "top-left":
            return styles["popup-tl"]
        case "top-right":
            return styles["popup-tr"]
        case "bottom-left":
            return styles["popup-bl"]
        case "bottom-right":
            return styles["popup-br"]
        case "left-top":
            return styles["popup-lt"]
        case "left-bottom":
            return styles["popup-lb"]
        case "right-top":
            return styles["popup-rt"]
        case "right-bottom":
            return styles["popup-rb"]
        default:
            return styles["popup-bl"]
    }
}

export default function Popup({
    trigger,
    triggerContainerClassName = "",
    containerClassName = "",
    popupContainerClassName = "",
    initialAnim = {},
    animate = {},
    exitAnim = {},
    alignment = "bottom-left",
    on = "click",
    children
}) {
    const [isOpen, setIsOpen] = useState(false);
    const popupRef = useRef(null);

    useEffect(() => {
        if (!isOpen) return;

        const handleClick = (e) => {
            if (popupRef.current && !popupRef.current.contains(e.target)) {
                setIsOpen(false);
            }
        }

        window.addEventListener("click", handleClick);

        return () => {
            window.removeEventListener("click", handleClick);
        }
    }, [isOpen])

    return (
        <div
            className={`relative ${containerClassName}`}
            onMouseEnter={() => { on == "hover" && setIsOpen(true) }}
            onMouseLeave={() => { on == "hover" && setIsOpen(false) }}
            ref={popupRef} >
            <div
                className={`${triggerContainerClassName}`}
                onClick={() => { if (on === "click") { setIsOpen(!isOpen) } }} >
                {trigger}
            </div>
            <AnimatePresence features={domAnimation}>
                {isOpen && (
                    <motion.div
                        initial={initialAnim}
                        animate={animate}
                        exit={exitAnim}
                        className={`absolute ${getPopupAlignmentUtilityClass(alignment)} ${popupContainerClassName}`} >
                        {children}
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    )
}