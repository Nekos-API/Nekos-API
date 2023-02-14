export function ScalePrimaryButton({ children, ...props }) {
    return (
        <button 
            className="text-white leading-none py-3 px-5 relative group flex-1" {...props}>
            <div className="absolute top-0 bottom-0 left-0 right-0 bg-crayola-350 rounded-full transition-transform group-hover:scale-105"></div>
            <div className="z-10 relative w-full flex flex-col items-center justify-center">{children}</div>
        </button>
    )
}

export function ScaleBorderButton({ children, ...props }) {
    return (
        <button className="text-neutral-800 leading-none py-3 px-5 relative group flex-1" {...props}>
            <div className="absolute top-0 bottom-0 left-0 right-0 border-2 border-neutral-200 rounded-full transition-transform group-hover:scale-105"></div>
            <div className="z-10 relative w-full flex flex-col items-center justify-center">{children}</div>
        </button>
    )
}

export function ScaleColoredButton({ color, textColor, children, ...props }) {
    return (
        <button className="leading-none py-3 px-5 relative group flex-1" style={{
            color: textColor
        }} {...props}>
            <div className="absolute top-0 bottom-0 left-0 right-0 rounded-full transition-transform group-hover:scale-105" style={{
                backgroundColor: color
            }}></div>
            <div className="z-10 relative w-full flex flex-col items-center justify-center">{children}</div>
        </button>
    )
}

export function LightPrimaryButton({ children, ...props }) {
    return (
        <button className="text-crayola-350 leading-none py-3 px-5 relative group flex-1" {...props}>
            <div className="absolute top-0 bottom-0 left-0 right-0 bg-crayola-100 rounded-full transition-transform group-hover:scale-105"></div>
            <div className="z-10 relative w-full flex flex-col items-center justify-center">{children}</div>
        </button>
    )
}

export function LightNeutralButton({ children, ...props }) {
    return (
        <button className="text-neutral-800 leading-none py-3 px-5 relative group flex-1" {...props}>
            <div className="absolute top-0 bottom-0 left-0 right-0 bg-neutral-100 rounded-full transition-transform group-hover:scale-105"></div>
            <div className="z-10 relative w-full flex flex-col items-center justify-center">{children}</div>
        </button>
    )
}

export function TextButton({ children, ...props }) {
    return (
        <button className="text-neutral-800 leading-none py-3 px-5 relative group flex-1" {...props}>
            <div className="absolute top-0 bottom-0 left-0 right-0 bg-white rounded-full transition-all scale-90 group-hover:scale-105 group-hover:bg-neutral-100"></div>
            <div className="z-10 relative w-full flex flex-col items-center justify-center">{children}</div>
        </button>
    )
}

export function IconButton({ children, ...props }) {
    return (
        <button className="text-neutral-800 leading-none p-3 relative group flex-1" {...props}>
            <div className="absolute top-0 bottom-0 left-0 right-0 bg-white rounded-full transition-all scale-90 group-hover:scale-105 group-hover:bg-neutral-100"></div>
            <div className="z-10 relative w-full flex flex-col items-center justify-center">{children}</div>
        </button>
    )
}