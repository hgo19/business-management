import { Loader } from "lucide-react"

export function Spinner({ className }: { className?: string }) {
  return (
    <Loader className={`h-4 w-4 animate-spin ${className}`} />
  )
}