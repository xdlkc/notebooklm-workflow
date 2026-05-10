import React from "react";
import {AbsoluteFill, Img, Sequence, interpolate, useCurrentFrame, useVideoConfig} from "remotion";

const stages = [
  ["00-06s", "问题开场", "一本书会散落成 PDF、笔记、PPT、音视频、链接。"],
  ["06-16s", "技能接力", "source、notebook、prompt、Studio、QA、delivery 分层协作。"],
  ["16-30s", "Notebook 核心", "等待 source ready，围绕同一 notebook 生成多种 artifact。"],
  ["30-42s", "审计与 QA", "留下 prompt log、artifact ID、manifest 和验证记录。"],
  ["42-54s", "交付分流", "原始大文件进 Drive，repo 只放压缩预览和说明。"],
  ["54-60s", "Demo", "README 直接浏览效果，Drive 打开原始文件。"],
];

export const NotebookLMWorkflowTeaser: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: "linear-gradient(135deg,#07111f,#312e81)", color: "white", fontFamily: "Inter, sans-serif"}}>
      <div style={{padding: 72}}>
        <h1 style={{fontSize: 64, margin: 0}}>NotebookLM Workflow</h1>
        <p style={{fontSize: 30, color: "#c7d2fe"}}>从一本书到 PPT、信息图、音视频与可复用 demo</p>
      </div>
      {stages.map(([time, title, body], i) => {
        const start = i * 10 * fps;
        const opacity = interpolate(frame, [start, start + 12, start + 10 * fps - 12, start + 10 * fps], [0, 1, 1, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
        const y = interpolate(frame, [start, start + 20], [40, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
        return (
          <Sequence key={title} from={start} durationInFrames={10 * fps}>
            <div style={{position: "absolute", left: 120, right: 120, bottom: 120, opacity, transform: `translateY(${y}px)`, padding: 48, borderRadius: 32, background: "rgba(255,255,255,.10)", border: "1px solid rgba(255,255,255,.22)"}}>
              <div style={{fontSize: 24, color: "#fde68a", fontFamily: "monospace"}}>{time}</div>
              <div style={{fontSize: 54, fontWeight: 800, marginTop: 12}}>{title}</div>
              <div style={{fontSize: 30, color: "#dbeafe", marginTop: 18}}>{body}</div>
            </div>
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
