import React from 'react';
import Link from 'next/link';
import { ChevronRightIcon, ChevronUpDownIcon, ArrowUpRightIcon } from '@heroicons/react/24/outline';
import JSIcon from '../icons/JS';
import styles from './index.module.css';


export function APIRequest({
    method = "GET",
    endpoint,
    title,
    description = "",
    parameters = [],
    responses = [],
    apiWrapperDocs = {}
}) {
    const hljs = require('highlight.js');

    const [collapsed, setCollapsed] = React.useState(true);
    const [openedResponse, setOpenedResponse] = React.useState(null);

    return (
        <div className={"w-full mt-8 p-4 rounded-lg drop-shadow-sm dark:drop-shadow-lg border border-neutral-200 dark:border-neutral-800 bg-neutral-50 dark:bg-neutral-900 group/request" + (collapsed ? " cursor-pointer" : "")} onClick={() => {
            if (collapsed) {
                setCollapsed(false);
            }
        }}>
            <button className='absolute top-3 right-3 p-1 rounded hover:bg-neutral-200 dark:hover:bg-neutral-800 transition-all' onClick={() => {
                setCollapsed(true);
            }}>
                <ChevronUpDownIcon className="h-6 w-6 transition" />
            </button>
            <div>
                <div className="flex flex-row items-center gap-2 leading-none">
                    <span className="text-sm font-bold text-[hsl(var(--nextra-primary-hue),100%,50%)]">{method}</span>
                    <span className="text-sm text-neutral-700 dark:text-neutral-200 font-mono">{endpoint}</span>
                </div>
                <div className="text-xl font-bold mt-2">{title}</div>
                <div className='mt-2'>{description}</div>
            </div>
            <div style={{
                display: collapsed ? 'none' : 'block'
            }}>
                <div className='mt-8'>
                    <div className='font-bold text-lg'>Parameters</div>
                    <div className='mt-1 flex flex-col gap-px bg-neutral-100 dark:bg-neutral-800 text-sm overflow-x-auto'>
                        {parameters.length > 0 ? parameters.map((value, index) => {
                            return (
                                <div className='text-neutral-600 dark:text-neutral-400 grid grid-cols-[1fr_1fr_minmax(0,2fr)] bg-neutral-50 dark:bg-neutral-900 py-1 items-center gap-4 min-w-[34rem]' key={index}>
                                    <div className='font-mono rounded bg-neutral-200 dark:bg-black/50 w-fit p-1 -my-1 block leading-none whitespace-nowrap'>
                                        {value.name}
                                        {value.required && <span className='text-red-500 inline-block ml-1'>*</span>}
                                    </div>
                                    <div className='whitespace-nowrap'>{value.type}</div>
                                    <div>{value.description}</div>
                                </div>
                            )
                        }) : (
                            <div className='bg-neutral-50 dark:bg-neutral-900 text-neutral-600 dark:text-neutral-400 pt-1'>No parameters</div>
                        )}
                    </div>
                </div>
                <div className='mt-8'>
                    <div className='font-bold text-lg'>Responses</div>
                    {responses.length > 0 ? (
                        <div className='flex flex-col gap-4 mt-4'>
                            {responses.map((value, index) => {
                                return (
                                    <div className={(value.example ? 'group/response hover:bg-neutral-100 dark:hover:bg-neutral-800 cursor-pointer' : 'cursor-default') + ' p-2 -m-2 rounded-lg transition ' + (openedResponse == index ? 'bg-neutral-100 dark:bg-neutral-800' : '')} onClick={() => {
                                        if (value.example) {
                                            if (openedResponse == index) {
                                                setOpenedResponse(null);
                                            } else {
                                                setOpenedResponse(index);
                                            }
                                        }
                                    }} key={index}>
                                        <div className='flex flex-row justify-between items-center'>
                                            <div>
                                                <div className={'font-bold transition ' + (openedResponse == index ? 'text-[hsl(var(--nextra-primary-hue),100%,50%)]' : ' text-neutral-700 dark:text-neutral-200 group-hover/response:text-[hsl(var(--nextra-primary-hue),100%,50%)]')}>{value.code}: {value.name}</div>
                                                <div className='text-neutral-600 dark:text-neutral-400 text-sm'>{value.description}</div>
                                            </div>
                                            {value.example && <ChevronRightIcon className={'h-5 w-5 transition-all ' + (openedResponse == index ? ' stroke-[hsl(var(--nextra-primary-hue),100%,50%)] rotate-90' : 'group-hover/response:stroke-[hsl(var(--nextra-primary-hue),100%,50%)]')} />}
                                        </div>
                                        {value.example && (
                                            <div className={'mt-4 rounded border dark:border-0 border-neutral-300 bg-neutral-50 dark:bg-neutral-900 '} style={{
                                                display: openedResponse == index ? 'block' : 'none'
                                            }}>
                                                <div className='p-2 border-b border-neutral-300 dark:border-neutral-800 text-sm text-neutral-600 dark:text-neutral-400 flex flex-row items-center gap-2'>
                                                    {value.example.headers.map((value, index) => {
                                                        return (
                                                            <span className='after:content-["·"] last:after:content-[""] after:text-neutral-400 dark:after:text-neutral-600 after:font-bold after:inline-block after:ml-2'>{value}</span>
                                                        )
                                                    })}
                                                </div>
                                                <pre dangerouslySetInnerHTML={{ __html: hljs.highlight(value.example.code, { language: value.example.language }).value }} className={styles.code + ' !p-2 overflow-x-auto'}></pre>
                                            </div>
                                        )}
                                    </div>
                                )
                            })}
                        </div>
                    ) : (
                        <div className='text-neutral-600 dark:text-neutral-400 pt-2'>No responses</div>
                    )}
                </div>
                <div className='mt-8'>
                    <div className='font-bold text-lg'>API Wrappers</div>
                    <div className='mt-2 flex flex-row items-center gap-2'>
                        {
                            apiWrapperDocs.python && (
                                <Link href={apiWrapperDocs.python} className='rounded border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 hover:border-neutral-400 dark:hover:border-neutral-600 dark:hover:bg-neutral-700 text-sm font-medium flex flex-row items-center leading-none p-2 gap-2 transition w-fit'>
                                    <img src="/imgs/logos/python.png" className="h-4 w-4 object-fit" />
                                    Python
                                    <ArrowUpRightIcon className='h-4 w-4 stroke-black dark:stroke-white' />
                                </Link>
                            )
                        }
                        {
                            apiWrapperDocs.javascript && (
                                <Link href={apiWrapperDocs.javascript} className='rounded border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 hover:border-neutral-400 dark:hover:border-neutral-600 dark:hover:bg-neutral-700 text-sm font-medium flex flex-row items-center leading-none p-2 gap-2 transition w-fit'>
                                    <div className='h-4 w-4 relative flex flex-col items-center'>
                                        <div className=' absolute block bg-black top-0.5 bottom-0.5 left-0.5 right-0.5'></div>
                                        <JSIcon className="h-4 w-4 fill-[#f0db4f] absolute" />
                                    </div>
                                    JavaScript
                                    <ArrowUpRightIcon className='h-4 w-4 stroke-black dark:stroke-white' />
                                </Link>
                            )
                        }
                        {!apiWrapperDocs.javascript && !apiWrapperDocs.python && (
                            <div className='text-neutral-600 dark:text-neutral-400 text-sm'>No wrapper support.</div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    )
}