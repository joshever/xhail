import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "XHAIL — Symbolic Learning Playground",
  description:
    "Interactive playground for XHAIL: eXtended Hybrid Abductive Inductive Learning. " +
    "Write logic programs, run the ILP pipeline, and see learned hypotheses in real time.",
  openGraph: {
    title: "XHAIL — Symbolic Learning Playground",
    description: "Inductive Logic Programming via Answer Set Programming, in your browser.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
